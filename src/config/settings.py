"""
Configurações do sistema de Service Desk.

Este módulo gerencia o carregamento de variáveis de ambiente e configurações
do sistema, incluindo chaves de API e flags de debug.
"""
import os
from pathlib import Path
from dotenv import load_dotenv


def load_environment_variables() -> None:
    """
    Carrega variáveis de ambiente do arquivo .env.
    
    Procura primeiro por .env na raiz do projeto. Se não encontrar,
    tenta carregar de .env.example como fallback.
    """
    project_root = Path(__file__).resolve().parents[2]
    dotenv_path = project_root / ".env"
    
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
    else:
        # Fallback: também carrega de .env.example se o usuário renomeou depois
        example_path = project_root / ".env.example"
        if example_path.exists():
            load_dotenv(example_path)


def get_required_env(name: str) -> str:
    """
    Obtém uma variável de ambiente obrigatória.
    
    Args:
        name: Nome da variável de ambiente
        
    Returns:
        Valor da variável de ambiente
        
    Raises:
        RuntimeError: Se a variável não estiver definida
    """
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variável de ambiente ausente: {name}")
    return value


# Carrega variáveis de ambiente ao importar o módulo
load_environment_variables()

# =============================================================================
# CONFIGURAÇÕES DO SISTEMA
# =============================================================================

# Chave da API do Google Gemini (obrigatória para funcionamento)
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

# Configurações opcionais do LangChain
LANGCHAIN_TRACING_V2: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")

# =============================================================================
# VALIDAÇÕES
# =============================================================================

def validar_configuracao() -> bool:
    """
    Valida se as configurações essenciais estão presentes.
    
    Returns:
        True se a configuração está válida, False caso contrário
    """
    return bool(GOOGLE_API_KEY)


def obter_info_configuracao() -> dict:
    """
    Retorna informações sobre o estado da configuração.
    
    Returns:
        Dict com informações de configuração
    """
    return {
        "google_api_key_configured": bool(GOOGLE_API_KEY),
        "langchain_tracing_enabled": LANGCHAIN_TRACING_V2,
        "langchain_api_key_configured": bool(LANGCHAIN_API_KEY),
    }


