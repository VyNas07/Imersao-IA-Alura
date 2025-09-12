import os
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import GOOGLE_API_KEY


def main() -> None:
	if not GOOGLE_API_KEY:
		raise RuntimeError("Defina GOOGLE_API_KEY no seu .env antes de executar.")

	llm = ChatGoogleGenerativeAI(
		model="gemini-1.5-flash",
		temperature=0.3,
		google_api_key=GOOGLE_API_KEY,
	)
	response = llm.invoke("Diga olá em português e se apresente brevemente de maneira criativa.")
	print(response.content)

	


if __name__ == "__main__":
	main()

