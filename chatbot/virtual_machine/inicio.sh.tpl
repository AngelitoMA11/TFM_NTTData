#!/bin/bash

# === TRAZABILIDAD ===
exec > /var/log/startup-script.log 2>&1
set -ex

echo "=== INICIO DEL SCRIPT DE ARRANQUE ==="

# === VARIABLES ===
project_id="${project_id}"
GCS_BUCKET="gs://rag-chroma-datos-${project_id}"
DATA_DIR="/opt/chroma_data"
MOUNT_POINT="/mnt/chroma"
EXCEL_FILE="chromadb_completa.xlsx"
DISK_PATH="/dev/disk/by-id/google-chroma-data"

echo "[1/8] Variables definidas."

# === ACTUALIZA SISTEMA E INSTALA DEPENDENCIAS ===
echo "[2/8] Actualizando sistema e instalando dependencias..."
apt-get update -y
apt-get install -y python3-pip git unzip

# === ESPERA Y MONTAJE DE DISCO ===
echo "[3/8] Formateando y montando disco persistente..."

for i in {1..5}; do
  if [[ -e "$DISK_PATH" ]]; then
    echo "Disco encontrado en intento $i"
    break
  fi
  echo "Esperando disco... intento $i"
  sleep 3
done

mkfs.ext4 -F "$DISK_PATH" || echo "mkfs.ext4 ya hecho o error"
mkdir -p "$MOUNT_POINT"
mount -o discard,defaults "$DISK_PATH" "$MOUNT_POINT"

chmod -R a+w "$MOUNT_POINT"

echo "[3/8] Disco montado y permisos corregidos."

# === CREA CARPETAS DE TRABAJO ===
echo "[4/8] Creando carpetas de trabajo..."
mkdir -p "$DATA_DIR"
cd "$DATA_DIR"

# === INSTALA DEPENDENCIAS PYTHON ===
echo "[5/8] Instalando dependencias Python..."
export TMPDIR="$MOUNT_POINT/tmp"
export TEMP="$TMPDIR"
export TMP="$TMPDIR"
mkdir -p "$TMPDIR"
chmod a+rwx "$TMPDIR"
echo "TMPDIR está configurado en: $TMPDIR"
ls -ld "$TMPDIR"

python3 -m pip install --upgrade pip --no-cache-dir
python3 -m pip install --no-cache-dir chromadb fastapi uvicorn pandas openpyxl sentence-transformers

# === DESCARGA ARCHIVO EXCEL ===
echo "[6/8] Descargando archivo Excel desde GCS..."

gsutil cp "$GCS_BUCKET/chroma/$EXCEL_FILE" . || { echo "Error descargando $EXCEL_FILE"; exit 1; }

[[ -f "$EXCEL_FILE" ]] || { echo "$EXCEL_FILE no existe tras la descarga"; exit 1; }

echo "Descarga Excel completada con éxito"

# === CREA SERVIDOR PYTHON FASTAPI ===
echo "[7/8] Creando servidor FastAPI..."

cat > app.py <<EOF
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

app = FastAPI()

client = chromadb.PersistentClient(path="$MOUNT_POINT")
embedding_fn = SentenceTransformerEmbeddingFunction("BAAI/bge-base-en")

def load_collection(name, excel_file, sheet_name):
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    collection = client.get_or_create_collection(name=name, embedding_function=embedding_fn)
    doc_column = 'documento'
    if doc_column not in df.columns:
        doc_column = df.columns[0]  # fallback to first column if 'document' not found
    for i, row in df.iterrows():
        collection.add(
            documents=[str(row[doc_column])],
            metadatas=[{"source": name}],
            ids=[f"{name}_{i}"]
        )

load_collection("modelos_llm", "$EXCEL_FILE", sheet_name="modelos_llm")
load_collection("opt_infra", "$EXCEL_FILE", sheet_name="opt_infra")

@app.get("/health")
def health():
    return {"status": "ok"}

class QueryRequest(BaseModel):
    text: str
    collection_name: str = "modelos_llm"

@app.post("/query")
def query(request: QueryRequest):
    collection = client.get_collection(name=request.collection_name)
    result = collection.query(query_texts=[request.text], n_results=3)
    return result
EOF

echo "app.py creado"

# === LANZA SERVIDOR ===
echo "[8/8] Iniciando servidor FastAPI con Uvicorn..."
cd "$DATA_DIR"
nohup uvicorn app:app --host 0.0.0.0 --port 8080 > server.log 2>&1 &

echo "Servidor iniciado"

echo "=== SCRIPT DE ARRANQUE FINALIZADO ==="
