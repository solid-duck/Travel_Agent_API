from fastapi import FastAPI, HTTPException

from app.agent import ask_agent
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(title='Travel Agent API', version='1.0.0')


@app.get('/health')
def health_check() -> dict[str, str]:
    print('[TRACE] Health check')
    return {'status': 'ok'}


@app.post('/chat', response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    print('[TRACE] POST /chat')
    try:
        return ChatResponse(answer=ask_agent(request.question))
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        print(f'[TRACE] Errore durante l esecuzione: {error}')
        raise HTTPException(status_code=502, detail='Il servizio del modello non ha restituito una risposta.') from error
