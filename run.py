"""
Script principal para executar o sistema de Service Desk com IA.

Este script oferece uma interface simples e direta para interagir com o sistema
de Service Desk que combina triagem automática e RAG para processar solicitações
de usuários e consultar políticas da empresa.

Uso:
    python run.py

Funcionalidades:
    - Triagem automática de mensagens
    - Consulta inteligente em políticas (RAG)
    - Recomendações baseadas em IA
    - Interface amigável no terminal

"""
from typing import Dict, Any
from src.agents import ServiceDeskAgent
from src.config.settings import GOOGLE_API_KEY, validar_configuracao


def exibir_cabecalho() -> None:
    """Exibe o cabeçalho do sistema."""
    print("🏢 SISTEMA DE SERVICE DESK - CARRARO DESENVOLVIMENTO")
    print("=" * 60)
    print("🤖 Sistema inteligente de triagem e consulta de políticas")
    print("=" * 60)


def verificar_configuracao() -> bool:
    """
    Verifica se a configuração está correta.
    
    Returns:
        True se a configuração está válida, False caso contrário
    """
    if not validar_configuracao():
        print("❌ Erro: GOOGLE_API_KEY não configurada no .env")
        print("💡 Crie um arquivo .env com: GOOGLE_API_KEY=sua_chave_aqui")
        print("📖 Consulte o README.md para mais informações")
        return False
    return True


def exibir_resultado(resultado: Dict[str, Any]) -> None:
    """
    Exibe o resultado do processamento de forma organizada.
    
    Args:
        resultado: Resultado do processamento da solicitação
    """
    # Informações de triagem
    print(f"\n📊 TRIAGEM:")
    print(f"   Decisão: {resultado['triagem']['decisão']}")
    print(f"   Urgência: {resultado['triagem']['urgencia']}")
    
    if resultado['triagem']['campos_faltantes']:
        print(f"   Campos faltantes: {', '.join(resultado['triagem']['campos_faltantes'])}")
    
    # Resposta do RAG (se disponível)
    if resultado['resposta_rag']:
        print(f"\n💡 RESPOSTA:")
        print(f"   {resultado['resposta_rag']}")
    
    # Recomendação e ação sugerida
    print(f"\n🎯 RECOMENDAÇÃO:")
    print(f"   {resultado['recomendacao']}")
    print(f"\n⚡ AÇÃO SUGERIDA: {resultado['acao_sugerida']}")
    
    # Documentos consultados
    if resultado['documentos_relevantes']:
        print(f"\n📄 Documentos consultados:")
        for doc in resultado['documentos_relevantes']:
            print(f"   • {doc['fonte'].split('/')[-1]}")


def processar_entrada_usuario(agent: ServiceDeskAgent) -> None:
    """
    Processa as entradas do usuário em loop contínuo.
    
    Args:
        agent: Instância do agente de Service Desk
    """
    print("✅ Sistema pronto! Digite suas perguntas ou 'sair' para encerrar.\n")
    
    while True:
        try:
            # Solicita entrada do usuário
            pergunta = input("👤 Você: ").strip()
            
            # Verifica se o usuário quer sair
            if pergunta.lower() in ['sair', 'exit', 'quit', '']:
                print("👋 Obrigado por usar o sistema! Até logo!")
                break
            
            # Processa a solicitação
            print("\n🤖 Processando...")
            resultado = agent.processar_solicitacao(pergunta)
            
            # Exibe o resultado
            exibir_resultado(resultado)
            print("\n" + "-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Sistema interrompido. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            print("Tente novamente ou digite 'sair' para encerrar.\n")


def main() -> None:
    """
    Função principal do sistema.
    
    Inicializa o sistema, verifica configurações e inicia o loop de interação
    com o usuário.
    """
    # Exibe cabeçalho
    exibir_cabecalho()
    
    # Verifica configuração
    if not verificar_configuracao():
        return
    
    try:
        # Inicializa o agente
        print("🤖 Inicializando agente...")
        agent = ServiceDeskAgent()
        agent.inicializar()
        
        # Inicia processamento de entradas
        processar_entrada_usuario(agent)
        
    except Exception as e:
        print(f"❌ Erro ao inicializar sistema: {e}")
        print("💡 Verifique se:")
        print("   - Os PDFs estão na pasta 'Pdf_Imersao_IA'")
        print("   - A GOOGLE_API_KEY está configurada")
        print("   - Todas as dependências estão instaladas")
        print("   - Você tem conexão com a internet")


if __name__ == "__main__":
    main()
