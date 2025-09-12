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

# Ponto de entrada do script: executa a função principal quando chamado diretamente
if __name__ == "__main__":
	main()