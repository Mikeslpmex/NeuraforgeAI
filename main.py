import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="NeuraforgeAI Gateway")

# Montar dashboard estático
app.mount("/dashboard", StaticFiles(directory="dashboard"), name="dashboard")

# Configurar API Key de Gemini
GENAI_API_KEY = os.getenv("GENAI_API_KEY", "TU_API_KEY_AQUI")
genai.configure(api_key=GENAI_API_KEY)

class ChatQuery(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home():
    return "<h1>🔱 NeuraforgeAI activo 🚀</h1>"

@app.post("/api/agente")
async def chat_agente(query: ChatQuery):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Usuario: {query.message}")
        return {"reply": response.text}
    except Exception:
        return {"reply": "Error conectando con Neuraforge. Revisa tu API Key."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
