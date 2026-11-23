# DARK FUTURO AI

Assistente educacional responsivo, com API FastAPI e interface instalável como PWA no Android.

## O que já funciona
- Interface responsiva para celular e computador.
- Perguntas digitadas e seleção de matéria.
- Envio de imagem (até 8 MB) para leitura da atividade.
- Respostas explicadas em português.
- Manifesto e service worker para instalação como aplicativo web no Android.
- Endpoint `/health` para monitoramento no Render.

## Rodar localmente
Requer Python 3.11 ou superior.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edite .env e coloque sua chave de API
uvicorn app:app --reload
```

Abra http://127.0.0.1:8000

## Publicar no Render
1. Envie todos os arquivos deste projeto para um repositório GitHub.
2. No Render, escolha **New + → Web Service** e conecte o repositório.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Em Environment, crie `OPENAI_API_KEY` com sua chave privada.
6. Deploy e teste `/health`.

Nunca coloque a chave da API no HTML, JavaScript, GitHub ou em mensagens públicas.

## Android
Esta primeira versão é um PWA: publique o site em HTTPS, abra o endereço no Chrome do Android e use o menu **Instalar app** ou **Adicionar à tela inicial**. Isso cria um atalho instalável com aparência de aplicativo. Um APK nativo pode ser empacotado depois, quando o site estiver publicado e testado.

## Próximas etapas antes de abrir ao público
- Adicionar login seguro, limites de uso e proteção contra abuso.
- Criar histórico persistente no banco de dados.
- Definir política de privacidade e regras de retenção de imagens.
- Configurar orçamento/limites na conta do provedor de IA.
- Testar acessibilidade, desempenho e respostas em várias matérias.

O projeto não acessa nem automatiza contas ou plataformas escolares externas.
