"""
Dados de teste para o sistema de triagem de Service Desk.
"""
from typing import List, Dict


# Casos de teste organizados por categoria
CASOS_TESTE_TRIAGEM: List[str] = [
    # Casos que devem ser AUTO_RESOLVER
    "Onde consultar as férias que eu tenho direito?",
    "Qual é a política de home office da empresa?",
    "Como funciona o reembolso de despesas de viagem?",
    "Qual o horário de funcionamento do refeitório?",
    
    # Casos que devem ser PEDIR_INFO
    "Como abrir um chamado?",
    "Como aprender mais sobre os processos da empresa?",
    "Preciso de ajuda com uma política",
    "Tenho uma dúvida sobre procedimentos",
    
    # Casos que devem ser ABRIR_CHAMADO
    "Último dia de pagamento é hoje e minha máquina quebrou, como solicito outra?",
    "Solicito exceção para trabalhar 5 dias remoto",
    "Preciso de liberação para acessar anexos externos",
    "Por favor, abra um chamado para o RH sobre meu salário",
    "Minha senha expirou e não consigo acessar o sistema",
]

# Casos de teste com resultados esperados para validação
CASOS_VALIDACAO: List[Dict[str, str]] = [
    {
        "mensagem": "Onde consultar as férias que eu tenho direito?",
        "decisao_esperada": "AUTO_RESOLVER",
        "urgencia_esperada": "BAIXA"
    },
    {
        "mensagem": "Como abrir um chamado?",
        "decisao_esperada": "PEDIR_INFO", 
        "urgencia_esperada": "MEDIA"
    },
    {
        "mensagem": "Último dia de pagamento é hoje e minha máquina quebrou, como solicito outra?",
        "decisao_esperada": "ABRIR_CHAMADO",
        "urgencia_esperada": "ALTA"
    }
]
