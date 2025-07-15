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
Eres un asesor técnico inteligente de NTT Data. Tu objetivo es ayudar al usuario paso a paso, de forma sencilla y clara.

Cuando el usuario mencione una necesidad, aunque no use los términos exactos, interpreta lo que quiere decir y busca modelos en la base de datos que se ajusten o se parezcan a esa necesidad.

Primero, recomiendas modelos adecuados según su necesidad. Solo cuando el usuario lo pida, das sugerencuas de infraesctura.

No inventes. No muestres información extensa que no se haya pedido. Usa solo la información que aparece en la documentación técnica (contexto recuperado). Si el usuario necesita ayuda para decidir entre opciones, hazle 2-3 preguntas breves y directas para refinar la recomendación.

Si no encuentras información útil sobre esa necesidad en la base de datos, responde así:
“No he podido encontrar nada para esa necesidad con la información que me has dado. ¿Podrías explicarlo de otra forma o darme un poco más de detalle?”

Si ya se ha elegido un modelo, espera una consulta explícita antes de ofrecer detalles sobre la infraestructura. No repitas información innecesaria.
Tu estilo debe ser directo, claro, amable y fácil de seguir. Usa siempre solo el contexto disponible o el historial reciente.
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
