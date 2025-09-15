"""
Ponto de entrada principal do sistema de triagem de Service Desk.
"""
from src.config.settings import GOOGLE_API_KEY
from src.chains import TriagemChain


def main() -> None:
    """
    Função principal que executa os testes do sistema de triagem.
    """
    # Validação: garante que a variável de ambiente com a chave da API está definida
    if not GOOGLE_API_KEY:
        raise RuntimeError("Defina GOOGLE_API_KEY no seu .env antes de executar.")
    
    # Inicializa a chain de triagem
    triagem_chain = TriagemChain()
    
    # Casos de teste para validação do sistema
    testes = [
        "Como abrir um chamado?",
        "Último dia de pagamento é hoje e minha máquina quebrou, como solicito outra?",
        "Como aprender mais sobre os processos da empresa?",
        "Onde consultar as férias que eu tenho direito?"
    ]
    
    print("=== Sistema de Triagem de Service Desk ===\n")
    
    for msg_teste in testes:
        resultado = triagem_chain.processar(msg_teste)
        print(f"Pergunta: {msg_teste}")
        print(f" -> Resposta: {resultado}\n")

# Ponto de entrada do script: executa a função principal quando chamado diretamente
if __name__ == "__main__":
	main()

