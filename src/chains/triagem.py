"""
Chain de triagem para classificação de mensagens do Service Desk.
"""
from typing import Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from src.config.settings import GOOGLE_API_KEY
from src.models import TriagemOut


# Prompt de triagem: instruções para classificar mensagens de Service Desk
TRIAGEM_PROMPT = (
    "Você é um triador de Service Desk para políticas internas da empresa Carraro Desenvolvimento. "
    "Dada a mensagem do usuário, retorne SOMENTE um JSON com:\n"
    "{\n"
    '  "decisao": "AUTO_RESOLVER" | "PEDIR_INFO" | "ABRIR_CHAMADO",\n'
    '  "urgencia": "BAIXA" | "MEDIA" | "ALTA",\n'
    '  "campos_faltantes": ["..."]\n'
    "}\n"
    "Regras:\n"
    '- **AUTO_RESOLVER**: Perguntas claras sobre regras ou procedimentos descritos nas políticas (Ex: "Posso reembolsar a internet do meu home office?", "Como funciona a política de alimentação em viagens?").\n'
    '- **PEDIR_INFO**: Mensagens vagas ou que faltam informações para identificar o tema ou contexto (Ex: "Preciso de ajuda com uma política", "Tenho uma dúvida geral").\n'
    '- **ABRIR_CHAMADO**: Pedidos de exceção, liberação, aprovação ou acesso especial, ou quando o usuário explicitamente pede para abrir um chamado (Ex: "Quero exceção para trabalhar 5 dias remoto.", "Solicito liberação para anexos externos.", "Por favor, abra um chamado para o RH.").'
    "Analise a mensagem e decida a ação mais apropriada."
)


class TriagemChain:
    """
    Chain responsável pela triagem e classificação de mensagens do Service Desk.
    """
    
    def __init__(self):
        """Inicializa a chain de triagem com o modelo Gemini."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=GOOGLE_API_KEY,
        )
        self.chain = self.llm.with_structured_output(TriagemOut)
    
    def processar(self, mensagem: str) -> Dict:
        """
        Processa uma mensagem e retorna a classificação de triagem.
        
        Args:
            mensagem: Texto da mensagem do usuário
            
        Returns:
            Dict com decisão, urgência e campos faltantes
        """
        saida: TriagemOut = self.chain.invoke([
            SystemMessage(content=TRIAGEM_PROMPT),
            HumanMessage(content=mensagem)
        ])
        return saida.model_dump()
