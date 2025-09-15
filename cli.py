"""
Interface de linha de comando para o sistema de Service Desk com IA.
Sistema integrado de triagem e RAG para consulta de políticas.
"""
import os
import sys
from typing import Optional
from src.config.settings import GOOGLE_API_KEY
from src.chains import TriagemChain
from src.tools.rag_local import RAGSystemLocal


class ServiceDeskCLI:
    """
    Interface de linha de comando para o sistema de Service Desk.
    """
    
    def __init__(self):
        """Inicializa o sistema CLI."""
        self.triagem_chain = None
        self.rag_system = None
        self.initialized = False
        
    def verificar_configuracao(self) -> bool:
        """Verifica se a configuração está correta."""
        if not GOOGLE_API_KEY:
            print("❌ Erro: GOOGLE_API_KEY não configurada no arquivo .env")
            print("💡 Crie um arquivo .env na raiz do projeto com:")
            print("   GOOGLE_API_KEY=sua_chave_aqui")
            return False
        return True
    
    def inicializar_sistemas(self) -> None:
        """Inicializa os sistemas de triagem e RAG."""
        if self.initialized:
            return
            
        print("🚀 Inicializando sistemas...")
        
        try:
            # Inicializa sistema de triagem
            print("🔧 Carregando sistema de triagem...")
            self.triagem_chain = TriagemChain()
            
            # Inicializa sistema RAG
            print("📚 Carregando sistema RAG...")
            self.rag_system = RAGSystemLocal()
            self.rag_system.inicializar()
            
            self.initialized = True
            print("✅ Sistemas inicializados com sucesso!\n")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar sistemas: {e}")
            sys.exit(1)
    
    def exibir_menu(self) -> None:
        """Exibe o menu principal."""
        print("=" * 60)
        print("🏢 SISTEMA DE SERVICE DESK - CARRARO DESENVOLVIMENTO")
        print("=" * 60)
        print("1. 📝 Fazer pergunta (Triagem + RAG)")
        print("2. 🔍 Apenas triagem (classificar mensagem)")
        print("3. 📚 Apenas consulta RAG (buscar em políticas)")
        print("4. 🧪 Executar testes automáticos")
        print("5. ℹ️  Informações do sistema")
        print("0. 🚪 Sair")
        print("=" * 60)
    
    def processar_pergunta_completa(self) -> None:
        """Processa uma pergunta usando triagem + RAG."""
        print("\n📝 MODO: Triagem + RAG")
        print("Digite sua pergunta ou solicitação:")
        pergunta = input("> ").strip()
        
        if not pergunta:
            print("❌ Pergunta não pode estar vazia.")
            return
        
        print("\n🔍 Processando...")
        
        try:
            # 1. Triagem
            resultado_triagem = self.triagem_chain.processar(pergunta)
            print(f"\n📊 TRIAGEM:")
            print(f"   Decisão: {resultado_triagem['decisão']}")
            print(f"   Urgência: {resultado_triagem['urgencia']}")
            if resultado_triagem['campos_faltantes']:
                print(f"   Campos faltantes: {', '.join(resultado_triagem['campos_faltantes'])}")
            
            # 2. RAG (se for AUTO_RESOLVER ou PEDIR_INFO)
            if resultado_triagem['decisão'] in ['AUTO_RESOLVER', 'PEDIR_INFO']:
                print(f"\n📚 CONSULTA RAG:")
                resultado_rag = self.rag_system.consultar(pergunta)
                print(f"   Resposta: {resultado_rag['resposta']}")
                
                if resultado_rag['documentos_relevantes']:
                    print(f"\n📄 Documentos consultados:")
                    for doc in resultado_rag['documentos_relevantes']:
                        print(f"   • {os.path.basename(doc['fonte'])}")
            
            # 3. Recomendação final
            print(f"\n💡 RECOMENDAÇÃO:")
            if resultado_triagem['decisão'] == 'AUTO_RESOLVER':
                print("   ✅ Esta pergunta pode ser respondida automaticamente com base nas políticas.")
            elif resultado_triagem['decisão'] == 'PEDIR_INFO':
                print("   ❓ Solicite mais informações específicas do usuário.")
            else:  # ABRIR_CHAMADO
                print("   🎫 Abra um chamado no sistema de Service Desk.")
                
        except Exception as e:
            print(f"❌ Erro ao processar pergunta: {e}")
    
    def processar_apenas_triagem(self) -> None:
        """Processa apenas a triagem de uma mensagem."""
        print("\n🔍 MODO: Apenas Triagem")
        print("Digite a mensagem para classificar:")
        mensagem = input("> ").strip()
        
        if not mensagem:
            print("❌ Mensagem não pode estar vazia.")
            return
        
        print("\n🔍 Classificando...")
        
        try:
            resultado = self.triagem_chain.processar(mensagem)
            
            print(f"\n📊 RESULTADO DA TRIAGEM:")
            print(f"   Decisão: {resultado['decisão']}")
            print(f"   Urgência: {resultado['urgencia']}")
            if resultado['campos_faltantes']:
                print(f"   Campos faltantes: {', '.join(resultado['campos_faltantes'])}")
            
            # Explicação da decisão
            print(f"\n💡 EXPLICAÇÃO:")
            if resultado['decisão'] == 'AUTO_RESOLVER':
                print("   Esta mensagem pode ser respondida automaticamente com base nas políticas da empresa.")
            elif resultado['decisão'] == 'PEDIR_INFO':
                print("   Esta mensagem precisa de mais informações para ser processada adequadamente.")
            else:  # ABRIR_CHAMADO
                print("   Esta mensagem requer abertura de um chamado no sistema de Service Desk.")
                
        except Exception as e:
            print(f"❌ Erro ao processar triagem: {e}")
    
    def processar_apenas_rag(self) -> None:
        """Processa apenas consulta RAG."""
        print("\n📚 MODO: Apenas Consulta RAG")
        print("Digite sua pergunta sobre políticas da empresa:")
        pergunta = input("> ").strip()
        
        if not pergunta:
            print("❌ Pergunta não pode estar vazia.")
            return
        
        print("\n🔍 Buscando nas políticas...")
        
        try:
            resultado = self.rag_system.consultar(pergunta)
            
            print(f"\n💡 RESPOSTA:")
            print(f"   {resultado['resposta']}")
            
            if resultado['documentos_relevantes']:
                print(f"\n📄 DOCUMENTOS CONSULTADOS:")
                for doc in resultado['documentos_relevantes']:
                    print(f"   • {os.path.basename(doc['fonte'])}")
                    print(f"     {doc['conteudo'][:100]}...")
                    
        except Exception as e:
            print(f"❌ Erro ao consultar RAG: {e}")
    
    def executar_testes_automaticos(self) -> None:
        """Executa testes automáticos do sistema."""
        print("\n🧪 MODO: Testes Automáticos")
        print("Executando testes do sistema...")
        
        # Testes de triagem
        print("\n🔍 Testando sistema de triagem...")
        testes_triagem = [
            "Como abrir um chamado?",
            "Último dia de pagamento é hoje e minha máquina quebrou, como solicito outra?",
            "Onde consultar as férias que eu tenho direito?",
            "Solicito exceção para trabalhar 5 dias remoto"
        ]
        
        for i, teste in enumerate(testes_triagem, 1):
            print(f"\n   Teste {i}: {teste}")
            try:
                resultado = self.triagem_chain.processar(teste)
                print(f"   ✅ {resultado['decisão']} - {resultado['urgencia']}")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
        
        # Testes de RAG
        print("\n📚 Testando sistema RAG...")
        testes_rag = [
            "Qual é a política de home office?",
            "Como funciona o reembolso de despesas?",
            "Quais são as regras de e-mail corporativo?"
        ]
        
        for i, teste in enumerate(testes_rag, 1):
            print(f"\n   Teste {i}: {teste}")
            try:
                resultado = self.rag_system.consultar(teste)
                print(f"   ✅ Resposta gerada ({len(resultado['resposta'])} caracteres)")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
        
        print("\n✅ Testes concluídos!")
    
    def exibir_informacoes_sistema(self) -> None:
        """Exibe informações sobre o sistema."""
        print("\nℹ️  INFORMAÇÕES DO SISTEMA")
        print("=" * 40)
        print(f"📊 Documentos carregados: {len(self.rag_system.docs)}")
        print(f"🔧 Sistema de triagem: ✅ Ativo")
        print(f"📚 Sistema RAG: ✅ Ativo")
        print(f"🤖 Modelo LLM: Gemini 1.5 Flash")
        print(f"🔍 Embeddings: HuggingFace (local)")
        print(f"📁 Pasta de PDFs: {self.rag_system.pdf_folder}")
        
        if self.rag_system.docs:
            print(f"\n📄 Documentos disponíveis:")
            for doc in self.rag_system.docs:
                fonte = doc.metadata.get('source', 'Desconhecida')
                print(f"   • {os.path.basename(fonte)}")
    
    def executar(self) -> None:
        """Executa o sistema CLI principal."""
        print("🏢 Sistema de Service Desk com IA - Carraro Desenvolvimento")
        print("Inicializando...\n")
        
        # Verifica configuração
        if not self.verificar_configuracao():
            return
        
        # Inicializa sistemas
        self.inicializar_sistemas()
        
        # Loop principal
        while True:
            try:
                self.exibir_menu()
                opcao = input("Escolha uma opção: ").strip()
                
                if opcao == "1":
                    self.processar_pergunta_completa()
                elif opcao == "2":
                    self.processar_apenas_triagem()
                elif opcao == "3":
                    self.processar_apenas_rag()
                elif opcao == "4":
                    self.executar_testes_automaticos()
                elif opcao == "5":
                    self.exibir_informacoes_sistema()
                elif opcao == "0":
                    print("\n👋 Obrigado por usar o sistema! Até logo!")
                    break
                else:
                    print("❌ Opção inválida. Tente novamente.")
                
                input("\n⏸️  Pressione Enter para continuar...")
                print("\n" + "="*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Sistema interrompido pelo usuário. Até logo!")
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}")
                input("Pressione Enter para continuar...")


def main():
    """Função principal."""
    cli = ServiceDeskCLI()
    cli.executar()


if __name__ == "__main__":
    main()
