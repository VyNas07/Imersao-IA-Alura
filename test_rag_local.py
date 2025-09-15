"""
Script de teste para o sistema RAG com embeddings locais.
Execute este arquivo para testar o sistema sem limites de quota.
"""
from src.tools.rag_local import RAGSystemLocal
from src.config.settings import GOOGLE_API_KEY


def main():
    """Função principal para testar o sistema RAG local."""
    print("🚀 Iniciando teste do sistema RAG (versão local)...")
    
    # Verifica se a API key está configurada
    if not GOOGLE_API_KEY:
        print("❌ Erro: GOOGLE_API_KEY não configurada no .env")
        return
    
    try:
        # Cria e inicializa o sistema RAG local
        print("🔧 Inicializando sistema RAG com embeddings locais...")
        print("⏳ Isso pode demorar um pouco na primeira execução (download do modelo)...")
        
        rag = RAGSystemLocal()
        rag.inicializar()
        
        print("\n" + "="*60)
        print("✅ Sistema RAG local inicializado com sucesso!")
        print("="*60)
        
        # Perguntas de teste
        perguntas_teste = [
            "Qual é a política de home office da empresa?",
            "Como funciona o reembolso de despesas de viagem?",
            "Quais são as regras de uso de e-mail corporativo?",
            "Posso trabalhar de casa todos os dias?",
            "Qual o limite de reembolso para alimentação em viagens?"
        ]
        
        print("\n🔍 Testando consultas...\n")
        
        for i, pergunta in enumerate(perguntas_teste, 1):
            print(f"📝 Pergunta {i}: {pergunta}")
            print("-" * 50)
            
            try:
                resultado = rag.consultar(pergunta)
                
                print(f"💡 Resposta: {resultado['resposta']}")
                print(f"\n📚 Documentos consultados:")
                for doc in resultado['documentos_relevantes']:
                    print(f"   • {doc['fonte']}")
                    print(f"     {doc['conteudo']}")
                
            except Exception as e:
                print(f"❌ Erro ao processar pergunta: {e}")
            
            print("\n" + "="*60 + "\n")
        
        print("🎉 Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante a inicialização: {e}")
        print("💡 Verifique se:")
        print("   - Os PDFs estão na pasta 'Pdf_Imersao_IA'")
        print("   - A GOOGLE_API_KEY está configurada")
        print("   - Todas as dependências estão instaladas")
        print("   - Você tem conexão com a internet (para download do modelo)")


if __name__ == "__main__":
    main()
