"""
Script de teste para o sistema LangGraph.

Testa o novo sistema de orquestração com LangGraph,
demonstrando fluxos condicionais e processamento inteligente.
"""
from src.agents import ServiceDeskAgent
from src.config.settings import GOOGLE_API_KEY


def testar_langgraph():
    """Testa o sistema LangGraph com diferentes cenários."""
    print("🚀 Testando Sistema LangGraph")
    print("=" * 60)
    
    # Verifica configuração
    if not GOOGLE_API_KEY:
        print("❌ Erro: GOOGLE_API_KEY não configurada no .env")
        return
    
    try:
        # Inicializa o agente
        print("🤖 Inicializando agente com LangGraph...")
        agent = ServiceDeskAgent()
        agent.inicializar()
        
        # Casos de teste
        casos_teste = [
            {
                "nome": "AUTO_RESOLVER - Pergunta sobre política",
                "mensagem": "Qual é a política de home office da empresa?",
                "esperado": "AUTO_RESOLVER"
            },
            {
                "nome": "PEDIR_INFO - Mensagem vaga",
                "mensagem": "Preciso de ajuda com uma política",
                "esperado": "PEDIR_INFO"
            },
            {
                "nome": "ABRIR_CHAMADO - Solicitação específica",
                "mensagem": "Minha máquina quebrou e preciso de uma nova urgente",
                "esperado": "ABRIR_CHAMADO"
            },
            {
                "nome": "AUTO_RESOLVER - Consulta sobre reembolso",
                "mensagem": "Como funciona o reembolso de despesas de viagem?",
                "esperado": "AUTO_RESOLVER"
            }
        ]
        
        print("\n🧪 Executando testes...\n")
        
        for i, caso in enumerate(casos_teste, 1):
            print(f"📝 Teste {i}: {caso['nome']}")
            print(f"   Mensagem: {caso['mensagem']}")
            print("-" * 50)
            
            try:
                # Processa a mensagem
                resultado = agent.processar_solicitacao(caso['mensagem'])
                
                # Exibe resultado
                print(f"   ✅ Decisão: {resultado['triagem']['decisão']}")
                print(f"   ✅ Urgência: {resultado['triagem']['urgencia']}")
                
                if resultado['resposta_rag']:
                    print(f"   ✅ RAG: {len(resultado['resposta_rag'])} caracteres")
                
                print(f"   ✅ Ação: {resultado['acao_sugerida']}")
                
                # Verifica se atendeu expectativa
                if resultado['triagem']['decisão'] == caso['esperado']:
                    print(f"   🎯 Resultado: CORRETO")
                else:
                    print(f"   ⚠️ Resultado: Esperado {caso['esperado']}, obtido {resultado['triagem']['decisão']}")
                
                # Exibe estatísticas se disponível
                if 'estatisticas' in resultado:
                    stats = resultado['estatisticas']
                    print(f"   📊 Estatísticas: {stats['tentativas']} tentativas, {stats['documentos_consultados']} docs")
                
            except Exception as e:
                print(f"   ❌ Erro: {e}")
            
            print("\n" + "=" * 60 + "\n")
        
        print("🎉 Testes concluídos!")
        
        # Teste de funcionalidades específicas
        print("\n🔧 Testando funcionalidades específicas...")
        
        # Teste de estatísticas
        print("\n📊 Teste de estatísticas:")
        stats = agent.obter_estatisticas("Qual é a política de home office?")
        print(f"   Fluxo executado: {stats['fluxo_executado']}")
        print(f"   Documentos consultados: {stats['documentos_consultados']}")
        
        # Teste de consulta direta
        print("\n📚 Teste de consulta direta RAG:")
        resultado_rag = agent.consultar_politicas("Como funciona o reembolso?")
        print(f"   Resposta: {resultado_rag['resposta'][:100]}...")
        
        # Teste de classificação direta
        print("\n🔍 Teste de classificação direta:")
        resultado_triagem = agent.classificar_mensagem("Preciso de ajuda")
        print(f"   Decisão: {resultado_triagem['decisão']}")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        print("💡 Verifique se:")
        print("   - Os PDFs estão na pasta 'Pdf_Imersao_IA'")
        print("   - A GOOGLE_API_KEY está configurada")
        print("   - Todas as dependências estão instaladas")


def demonstrar_fluxo_condicional():
    """Demonstra o fluxo condicional do LangGraph."""
    print("\n🔄 Demonstração de Fluxo Condicional")
    print("=" * 60)
    
    agent = ServiceDeskAgent()
    agent.inicializar()
    
    # Mensagem que deve gerar PEDIR_INFO
    mensagem = "Preciso de ajuda"
    print(f"📝 Mensagem: {mensagem}")
    
    resultado = agent.processar_solicitacao(mensagem)
    
    print(f"\n📊 Resultado:")
    print(f"   Decisão: {resultado['triagem']['decisão']}")
    print(f"   Tentativas: {resultado['tentativas']}")
    print(f"   Fluxo: {resultado['estatisticas']['fluxo_executado']}")
    
    if resultado['triagem']['decisão'] == 'PEDIR_INFO':
        print(f"\n✅ Fluxo condicional funcionando!")
        print(f"   O sistema identificou que precisa de mais informações")
        print(f"   e seguiu o fluxo correto: triagem → solicitar_info → finalizar")


if __name__ == "__main__":
    testar_langgraph()
    demonstrar_fluxo_condicional()
