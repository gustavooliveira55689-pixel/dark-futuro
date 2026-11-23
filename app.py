import os
from pathlib import Path
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from ai_solver import answer_question, answer_from_image

load_dotenv()
app = FastAPI(title="DARK FUTURO AI")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok", "app": "DARK FUTURO AI"}

@app.post("/api/solve")
async def solve(payload: dict):
    question = str(payload.get("question", "")).strip()
    subject = str(payload.get("subject", "Geral")).strip()[:60]
    if not question:
        return JSONResponse({"error": "Escreva uma questão primeiro."}, status_code=400)
    try:
        result = await answer_question(question, subject)
        return {"answer": result}
    except Exception as exc:
        # Não expõe detalhes internos nem chaves ao navegador.
        print("AI error:", repr(exc))
        return JSONResponse(
            {"error": "Não foi possível consultar a IA agora. Confira a chave da API no Render."},
            status_code=503
        )

@app.post("/api/image")
async def solve_image(file: UploadFile = File(...), subject: str = Form("Geral")):
    if not file.content_type or not file.content_type.startswith("image/"):
        return JSONResponse({"error": "Envie uma imagem (JPG, PNG ou WEBP)."}, status_code=400)
    data = await file.read()
    if len(data) > 8 * 1024 * 1024:
        return JSONResponse({"error": "A imagem deve ter até 8 MB."}, status_code=413)
    try:
        result = await answer_from_image(data, file.content_type, subject)
        return {"answer": result}
    except Exception as exc:
        print("Image AI error:", repr(exc))
        return JSONResponse(
            {"error": "Não foi possível analisar a imagem. Confira a chave da API e tente novamente."},
            status_code=503
        )
