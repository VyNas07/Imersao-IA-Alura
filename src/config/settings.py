import os
from pathlib import Path
from dotenv import load_dotenv


def load_environment_variables() -> None:
	"""Load .env file from project root if present."""
	project_root = Path(__file__).resolve().parents[2]
	dotenv_path = project_root / ".env"
	if dotenv_path.exists():
		load_dotenv(dotenv_path)
	else:
		# Fallback: also load from .env.example if user renamed later
		example_path = project_root / ".env.example"
		if example_path.exists():
			load_dotenv(example_path)


def get_required_env(name: str) -> str:
	value = os.getenv(name)
	if not value:
		raise RuntimeError(f"Variável de ambiente ausente: {name}")
	return value


# Carrega variáveis logo ao importar o módulo
load_environment_variables()

# Chaves e flags
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
LANGCHAIN_TRACING_V2: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")


