import os
import base64
from openai import AsyncOpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SYSTEM_PROMPT = """
Você é o DARK FUTURO AI, um tutor escolar paciente e claro, em português do Brasil.
Ajude estudantes de diferentes níveis e matérias. Resolva exercícios mostrando:
1. O que a questão pede.
2. O raciocínio e as etapas necessárias.
3. A resposta final, claramente identificada.
Se faltar informação, diga o que está faltando. Não invente dados.
Priorize ensinar, não apenas entregar respostas. Use linguagem adequada à idade.
"""

def get_client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY não configurada")
    return AsyncOpenAI(api_key=key)

async def answer_question(question: str, subject: str) -> str:
    client = get_client()
    response = await client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=f"Matéria: {subject}\nQuestão do estudante:\n{question}"
    )
    return response.output_text

async def answer_from_image(image_bytes: bytes, mime_type: str, subject: str) -> str:
    client = get_client()
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    response = await client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT + "\nLeia cuidadosamente o enunciado da imagem. Se algo estiver ilegível, avise.",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": f"Analise e explique a atividade. Matéria: {subject}."},
                {"type": "input_image", "image_url": f"data:{mime_type};base64,{encoded}"}
            ]
        }]
    )
    return response.output_text
