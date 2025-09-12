# Imports das bibliotecas necessárias e configuração de tipos/validação
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import GOOGLE_API_KEY
from pydantic import BaseModel, Field
from typing import List, Literal, Dict



def main() -> None:
	# Validação: garante que a variável de ambiente com a chave da API está definida
	if not GOOGLE_API_KEY:
		raise RuntimeError("Defina GOOGLE_API_KEY no seu .env antes de executar.")

	# Instancia o cliente do modelo generativo (Gemini) com parâmetros de inferência
	llm = ChatGoogleGenerativeAI(
		model="gemini-1.5-flash",
		temperature=0.3,
		google_api_key=GOOGLE_API_KEY,
	)

	# Faz uma chamada simples ao modelo para validar a integração
	response = llm.invoke("Diga olá em português e se apresente brevemente de maneira criativa.")

	# Exibe o conteúdo retornado pelo modelo no console
	print(response.content)

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
	
# Esquema de saída da triagem usando Pydantic para validação de tipos
class TriagemOut(BaseModel):
	decisão: Literal["AUTO_RESOLVER", "PEDIR_INFO", "ABRIR_CHAMADO"]
	urgencia: Literal["BAIXA", "MEDIA", "ALTA"]
	campos_faltantes: List[str] = Field(default_factory=list)


# Ponto de entrada do script: executa a função principal quando chamado diretamente
if __name__ == "__main__":
	main()

