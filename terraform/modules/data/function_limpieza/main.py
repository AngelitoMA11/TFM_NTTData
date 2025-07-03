import os
import pandas as pd
import datetime
from flask import Request, jsonify
from google.cloud import bigquery
import logging

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET = os.getenv("DATASET")
TABLE = os.getenv("TABLE")

def limpiar_execution_id(df):
    df['execution_id'] = range(1, len(df) + 1)
    return df

def limpiar_model_id(df):
    if 'model_id' in df.columns:
        df['model_id'] = df['model_id'].fillna(0).astype(int)
    return df

def limpiar_execution_date(df):
    if 'execution_date' not in df.columns:
        df['execution_day'] = None
        df['execution_time'] = 'Desconocida'
        return df

    df['execution_date'] = pd.to_datetime(df['execution_date'], errors='coerce')
    df['execution_time'] = None

    for idx in df[df['execution_date'].isnull()].index:
        prev = df['execution_date'].iloc[idx - 1] if idx > 0 else None
        next_ = df['execution_date'].iloc[idx + 1] if idx + 1 < len(df) else None
        if pd.notnull(prev) and pd.notnull(next_) and prev.date() == next_.date():
            df.at[idx, 'execution_date'] = pd.Timestamp(f"{prev.date()} 00:00:00")
        df.at[idx, 'execution_time'] = 'Desconocida'

    df['execution_day'] = df['execution_date'].dt.date
    df['execution_time'] = df['execution_date'].dt.time.where(df['execution_time'] != 'Desconocida', 'Desconocida')
    df.drop(columns=['execution_date'], inplace=True)
    return df

def limpiar_oficina(df):
    if 'oficina' in df.columns:
        reemplazos = {
            'LIS': 'Lisboa',
            'MAD': 'Madrid',
            'BCN': 'Barcelona',
            'valència': 'Valencia'
        }
        df['oficina'] = df['oficina'].replace(reemplazos)
        df['oficina'] = df['oficina'].fillna('Desconocido')
    return df

def normalizar_columna(df, col):
    if col in df.columns and df[col].dtype == object:
        df[col] = df[col].str.replace(',', '.', regex=False)
    return pd.to_numeric(df[col], errors='coerce') if col in df.columns else df

def recalcular_kpis(df):
    columnas = [
        'energy_epoch_wh', 'num_epochs', 'emission_factor_location',
        'total_inference_energy_wh', 'num_predictions', 'model_accuracy',
        'total_data', 'data_used', 'cpt_kg_co2', 'ept_kwh', 'model_size_mb'
    ]
    for col in columnas:
        if col in df.columns:
            df[col] = normalizar_columna(df, col)

    def rellenar(col, cond, formula):
        df.loc[cond, col] = formula

    if {'energy_epoch_wh', 'power_usage_w', 'duration_epoch_h'}.issubset(df.columns):
        m = df['energy_epoch_wh'].isna() & df['power_usage_w'].notna() & df['duration_epoch_h'].notna()
        rellenar('energy_epoch_wh', m, df.loc[m, 'power_usage_w'] * df.loc[m, 'duration_epoch_h'])

    if {'ept_kwh', 'energy_epoch_wh', 'num_epochs'}.issubset(df.columns):
        m = df['ept_kwh'].isna() & df['energy_epoch_wh'].notna() & df['num_epochs'].notna()
        rellenar('ept_kwh', m, (df.loc[m, 'energy_epoch_wh'] * df.loc[m, 'num_epochs']) / 1000)

    if {'cpt_kg_co2', 'ept_kwh', 'emission_factor_location'}.issubset(df.columns):
        m = df['cpt_kg_co2'].isna() & df['ept_kwh'].notna() & df['emission_factor_location'].notna()
        rellenar('cpt_kg_co2', m, df.loc[m, 'ept_kwh'] * df.loc[m, 'emission_factor_location'])

    if {'epp_wh', 'total_inference_energy_wh', 'num_predictions'}.issubset(df.columns):
        m = df['epp_wh'].isna() & df['total_inference_energy_wh'].notna() & df['num_predictions'].notna()
        rellenar('epp_wh', m, df.loc[m, 'total_inference_energy_wh'] / df.loc[m, 'num_predictions'])

    if {'ce', 'model_accuracy', 'cpt_kg_co2'}.issubset(df.columns):
        m = df['ce'].isna() & df['model_accuracy'].notna() & df['cpt_kg_co2'].notna()
        rellenar('ce', m, df.loc[m, 'model_accuracy'] / df.loc[m, 'cpt_kg_co2'])

    if {'dwr', 'total_data', 'data_used'}.issubset(df.columns):
        m = df['dwr'].isna() & df['total_data'].notna() & df['data_used'].notna()
        rellenar('dwr', m, (df.loc[m, 'total_data'] - df.loc[m, 'data_used']) / df.loc[m, 'total_data'])

    if {'mfs', 'cpt_kg_co2', 'model_accuracy'}.issubset(df.columns):
        m = df['mfs'].isna() & df['cpt_kg_co2'].notna() & df['model_accuracy'].notna()
        rellenar('mfs', m, df.loc[m, 'cpt_kg_co2'] * (1 - df.loc[m, 'model_accuracy']))

    if {'ept_per_mb', 'ept_kwh', 'model_size_mb'}.issubset(df.columns):
        m = df['ept_per_mb'].isna() & df['ept_kwh'].notna() & df['model_size_mb'].notna()
        rellenar('ept_per_mb', m, df.loc[m, 'ept_kwh'] / df.loc[m, 'model_size_mb'])

    if {'cpt_per_mb', 'cpt_kg_co2', 'model_size_mb'}.issubset(df.columns):
        m = df['cpt_per_mb'].isna() & df['cpt_kg_co2'].notna() & df['model_size_mb'].notna()
        rellenar('cpt_per_mb', m, df.loc[m, 'cpt_kg_co2'] / df.loc[m, 'model_size_mb'])
    if {'ce', 'mfs'}.issubset(df.columns):
        df['indice_sostenibilidad'] = df.apply(
            lambda row: row['ce'] / row['mfs'] if pd.notnull(row['ce']) and pd.notnull(row['mfs']) and row['mfs'] != 0 else None,
            axis=1
        )

    return df

def insertar_en_bigquery(df):
    client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET}.{TABLE}"
    
    # Claves únicas para comparar duplicados
    claves = ["Model_id", "Execution_id"]

    # Leer claves existentes desde BigQuery
    query = f"""
        SELECT {', '.join(claves)}
        FROM `{table_id}`
    """
    try:
        existentes = client.query(query).to_dataframe()
        df = df.merge(existentes, on=claves, how='left', indicator=True)
        df = df[df['_merge'] == 'left_only'].drop(columns=['_merge'])
    except Exception as e:
        logging.warning(f"No se pudo leer claves existentes: {e}. Se insertarán todos los registros.")

    if df.empty:
        logging.info("No hay registros nuevos para insertar.")
        return "No se insertó ningún registro: todos eran duplicados."

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        autodetect=True
    )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    return f"{len(df)} registros insertados en {table_id}"

def main(request: Request):
    try:
        logging.info("Inicio de la función")

        if request.method != "POST":
            logging.warning("Método no permitido")
            return jsonify({"error": "Solo se acepta POST"}), 405

        logging.info("Leyendo CSV del request")
        df = pd.read_csv(request.files['file']) if request.content_type.startswith("multipart/form-data") else pd.read_csv(request.stream)
        logging.info(f"DataFrame cargado con {len(df)} filas y {len(df.columns)} columnas")

        df.columns = [str(col).strip().lower() for col in df.columns]
        df = df.loc[:, ~df.columns.duplicated()]

        logging.info("Aplicando funciones de limpieza")
        df = limpiar_execution_id(df)
        df = limpiar_model_id(df)
        df = limpiar_execution_date(df)
        df = limpiar_oficina(df)
        df = recalcular_kpis(df)

        for col in ['dwr', 'cpt_per_mb']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

        logging.info("Renombrando columnas")
        columnas_a_renombrar = {
            'execution_id': 'Execution_id', 
            'model_id': 'Model_id',
            'execution_day': 'Execution_day', 
            'execution_time': 'Execution_time',
            'oficina': 'Oficina', 
            'power_usage_w': 'Power_usage_w',
            'duration_epoch_h': 'Duration_epoch_h', 
            'num_epochs': 'Num_epochs',
            'emission_factor_location': 'Emission_factor_location',
            'total_inference_energy_wh': 'Total_inference_energy_wh',
            'num_predictions': 'Num_predictions', 
            'model_accuracy': 'Model_accuracy',
            'total_data': 'Total_data', 
            'data_used': 'Data_used',
            'model_size_mb': 'Model_size_mb', 
            'energy_epoch_wh': 'Energy_epoch_Wh',
            'ept_kwh': 'EPT_kwh', 
            'cpt_kg_co2': 'CPT_kg_co2', 
            'epp_wh': 'Epp_wh',
            'ce': 'Carbon_efficiency', 
            'dwr': 'Data_Waste_Ratio',
            'mfs': 'Model_Footprint_Score', 
            'ept_per_mb': 'EPT_per_mb',
            'cpt_per_mb': 'CPT_per_mb',
            'indice_sostenibilidad': 'Indice_Sostenibilidad'

        }
        df.rename(columns={k: v for k, v in columnas_a_renombrar.items() if k in df.columns}, inplace=True)

        if 'Execution_time' in df.columns:
            df['Execution_time'] = df['Execution_time'].apply(
                lambda x: x.strftime('%H:%M:%S') if isinstance(x, datetime.time) else str(x)
            )
        if 'Execution_day' in df.columns:
            df['Execution_day'] = pd.to_datetime(df['Execution_day'], errors='coerce').dt.date

        df_validos = df[df['Model_id'].notna()]
        logging.info(f"Filas válidas para insertar: {len(df_validos)}")

        resultado = insertar_en_bigquery(df_validos)
        logging.info("Inserción en BigQuery completada")

        return jsonify({"message": resultado}), 200

    except Exception as e:
        logging.exception("Error en la ejecución")
        return jsonify({"error": str(e)}), 500