"""
Script principal para executar o sistema de Service Desk.
Execute: python run.py
"""
from src.agents import ServiceDeskAgent
from src.config.settings import GOOGLE_API_KEY


def main():
    """Função principal simplificada."""
    print("🏢 SISTEMA DE SERVICE DESK - CARRARO DESENVOLVIMENTO")
    print("=" * 60)
    
    # Verifica configuração
    if not GOOGLE_API_KEY:
        print("❌ Erro: GOOGLE_API_KEY não configurada no .env")
        print("💡 Crie um arquivo .env com: GOOGLE_API_KEY=sua_chave_aqui")
        return
    
    try:
        # Inicializa o agente
        print("🤖 Inicializando agente...")
        agent = ServiceDeskAgent()
        agent.inicializar()
        
        print("✅ Sistema pronto! Digite suas perguntas ou 'sair' para encerrar.\n")
        
        # Loop principal
        while True:
            try:
                pergunta = input("👤 Você: ").strip()
                
                if pergunta.lower() in ['sair', 'exit', 'quit', '']:
                    print("👋 Obrigado por usar o sistema! Até logo!")
                    break
                
                print("\n🤖 Processando...")
                
                # Processa a solicitação
                resultado = agent.processar_solicitacao(pergunta)
                
                # Exibe resultado
                print(f"\n📊 TRIAGEM:")
                print(f"   Decisão: {resultado['triagem']['decisão']}")
                print(f"   Urgência: {resultado['triagem']['urgencia']}")
                
                if resultado['triagem']['campos_faltantes']:
                    print(f"   Campos faltantes: {', '.join(resultado['triagem']['campos_faltantes'])}")
                
                if resultado['resposta_rag']:
                    print(f"\n💡 RESPOSTA:")
                    print(f"   {resultado['resposta_rag']}")
                
                print(f"\n🎯 RECOMENDAÇÃO:")
                print(f"   {resultado['recomendacao']}")
                
                print(f"\n⚡ AÇÃO SUGERIDA: {resultado['acao_sugerida']}")
                
                if resultado['documentos_relevantes']:
                    print(f"\n📄 Documentos consultados:")
                    for doc in resultado['documentos_relevantes']:
                        print(f"   • {doc['fonte'].split('/')[-1]}")
                
                print("\n" + "-" * 60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Sistema interrompido. Até logo!")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
                print("Tente novamente ou digite 'sair' para encerrar.\n")
    
    except Exception as e:
        print(f"❌ Erro ao inicializar sistema: {e}")
        print("💡 Verifique se:")
        print("   - Os PDFs estão na pasta 'Pdf_Imersao_IA'")
        print("   - A GOOGLE_API_KEY está configurada")
        print("   - Todas as dependências estão instaladas")


if __name__ == "__main__":
    main()
