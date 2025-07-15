import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

# Claves y config
CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_PORT = os.getenv("CHROMA_PORT")
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

# FastAPI app
app = FastAPI()
historial_global = []

SYSTEM_PROMPT = """
Eres un asesor técnico inteligente de NTT Data. Tu objetivo es ayudar al usuario paso a paso.

Primero, recomiendas modelos adecuados según su necesidad. Solo cuando el usuario lo pida, das sugerencias de infraestructura.

No muestres información extensa que no se ha pedido. Si el usuario necesita ayuda para decidir entre opciones, hazle 2-3 preguntas breves y directas para refinar la recomendación.

Si ya se ha elegido un modelo, espera una consulta explícita antes de ofrecer detalles de infraestructura. No repitas información innecesaria. Ofrece recomendaciones prácticas, breves y claras, como si estuvieras respondiendo por correo a un equipo técnico.

Utiliza solo la información principal que te de la base de datos
"""

class Pregunta(BaseModel):
    text: str

def retrieve_context(query, k=3):
    try:
        context = []

        for coleccion in ["modelos_llm", "opt_infra"]:
            url = f"http://{CHROMA_HOST}:{CHROMA_PORT}/query"
            response = requests.post(url, json={"text": query, "collection_name": coleccion}, timeout=5)
            response.raise_for_status()
            result = response.json()
            docs = result.get("documents", [[]])[0]
            context.extend(docs)

        return context
    except Exception as e:
        print(f"Error recuperando contexto: {e}")
        return []

def build_prompt_unificado(query, context_chunks, historial):
    context = "\n\n".join(context_chunks) if context_chunks else ""

    if historial:
        history_text = "\n".join(f"Usuario: {user}\nAsesor: {bot}" for user, bot in historial)
        historial_section = f"Historial de conversación:\n{history_text}\n"

        ultima_pregunta, ultima_respuesta = historial[-1]
        pista = f"\nNOTA: El usuario podría estar refiriéndose a temas o modelos mencionados en la última respuesta:\n{ultima_respuesta[:300]}\n"
        historial_section += f"\n{pista}\n"
    else:
        historial_section = ""

    context_section = f"Documentación técnica relevante:\n{context}\n" if context else ""

    return f"""{SYSTEM_PROMPT}

{historial_section}
{context_section}
Consulta actual del usuario:
{query}

Tu respuesta:"""

def generate_answer(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

@app.post("/preguntar")
def preguntar(pregunta: Pregunta):
    query = pregunta.text
    context = retrieve_context(query)
    prompt = build_prompt_unificado(query, context, historial_global)
    respuesta = generate_answer(prompt)
    historial_global.append((query, respuesta))
    return {
        "respuesta": respuesta
    }
