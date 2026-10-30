import os

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from app.tools import TRAVEL_TOOLS

load_dotenv()


def build_agent() -> AgentExecutor:
    """Costruisce l'agente LangChain e collega i tool di viaggio."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'replace_with_your_api_key':
        raise RuntimeError('OPENAI_API_KEY non configurata. Copia .env.example in .env e inserisci la chiave.')

    model_name = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    print(f'[TRACE] Creazione agente con modello: {model_name}')
    model = ChatOpenAI(model=model_name, temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'Sei un assistente di viaggio chiaro e prudente. Rispondi in italiano. Usa i tool quando servono e non inventare dati.'),
        ('human', '{input}'),
        MessagesPlaceholder(variable_name='agent_scratchpad'),
    ])
    agent = create_tool_calling_agent(model, TRAVEL_TOOLS, prompt)
    return AgentExecutor(agent=agent, tools=TRAVEL_TOOLS, verbose=True)


def ask_agent(question: str) -> str:
    print(f'[TRACE] Domanda ricevuta: {question}')
    result = build_agent().invoke({'input': question})
    print('[TRACE] Risposta generata')
    return result.get('output', 'Non ho ricevuto una risposta.')
