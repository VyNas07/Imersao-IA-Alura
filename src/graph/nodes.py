"""
Nós do grafo LangGraph para processamento de Service Desk.

Cada nó representa uma etapa específica do processamento e recebe
o estado atual, processa e retorna o estado atualizado.
"""
from typing import Dict, Any
from src.graph.state import ServiceDeskState
from src.chains import TriagemChain
from src.tools.rag_local import RAGSystemLocal


class ServiceDeskNodes:
    """
    Classe que contém todos os nós do grafo de Service Desk.
    
    Cada método representa um nó do grafo e recebe o estado atual,
    processa a informação e retorna o estado atualizado.
    """
    
    def __init__(self):
        """Inicializa os nós com as dependências necessárias."""
        self.triagem_chain = TriagemChain()
        self.rag_system = None  # Será inicializado quando necessário
    
    def _inicializar_rag(self) -> None:
        """Inicializa o sistema RAG se ainda não foi inicializado."""
        if self.rag_system is None:
            self.rag_system = RAGSystemLocal()
            self.rag_system.inicializar()
    
    def executar_triagem(self, state: ServiceDeskState) -> ServiceDeskState:
        """
        Nó de triagem: classifica a mensagem do usuário.
        
        Args:
            state: Estado atual do grafo
            
        Returns:
            Estado atualizado com resultado da triagem
        """
        try:
            print("🔍 Executando triagem...")
            
            # Executa a triagem
            resultado_triagem = self.triagem_chain.processar(state.mensagem_original)
            
            # Atualiza o estado
            state.triagem = resultado_triagem
            state.decisao = resultado_triagem['decisão']
            state.urgencia = resultado_triagem['urgencia']
            state.campos_faltantes = resultado_triagem['campos_faltantes']
            
            # Determina se precisa de mais informações
            state.precisa_mais_info = state.decisao == "PEDIR_INFO"
            
            print(f"✅ Triagem concluída: {state.decisao} - {state.urgencia}")
            
        except Exception as e:
            state.erro = f"Erro na triagem: {e}"
            print(f"❌ Erro na triagem: {e}")
        
        return state
    
    def executar_rag(self, state: ServiceDeskState) -> ServiceDeskState:
        """
        Nó de RAG: busca informações nas políticas da empresa.
        
        Args:
            state: Estado atual do grafo
            
        Returns:
            Estado atualizado com resposta do RAG
        """
        try:
            # Só executa RAG se for AUTO_RESOLVER ou PEDIR_INFO
            if state.decisao not in ["AUTO_RESOLVER", "PEDIR_INFO"]:
                print("⏭️ Pulando RAG - não necessário para esta decisão")
                return state
            
            print("📚 Executando busca RAG...")
            
            # Inicializa RAG se necessário
            self._inicializar_rag()
            
            # Executa a busca
            resultado_rag = self.rag_system.consultar(state.mensagem_original)
            
            # Atualiza o estado
            state.resposta_rag = resultado_rag['resposta']
            state.documentos_relevantes = resultado_rag['documentos_relevantes']
            
            print(f"✅ RAG concluído: {len(state.documentos_relevantes)} documentos consultados")
            
        except Exception as e:
            state.erro = f"Erro no RAG: {e}"
            print(f"❌ Erro no RAG: {e}")
        
        return state
    
    def gerar_recomendacao(self, state: ServiceDeskState) -> ServiceDeskState:
        """
        Nó de recomendação: gera recomendação baseada na análise.
        
        Args:
            state: Estado atual do grafo
            
        Returns:
            Estado atualizado com recomendação
        """
        try:
            print("💡 Gerando recomendação...")
            
            # Gera recomendação baseada na decisão
            if state.decisao == "AUTO_RESOLVER":
                if state.resposta_rag:
                    state.recomendacao = (
                        "✅ Esta solicitação pode ser respondida automaticamente. "
                        f"Resposta baseada nas políticas: {state.resposta_rag[:200]}..."
                    )
                else:
                    state.recomendacao = (
                        "✅ Esta solicitação pode ser respondida automaticamente "
                        "com base nas políticas da empresa."
                    )
                state.acao_sugerida = "Responder automaticamente"
                
            elif state.decisao == "PEDIR_INFO":
                campos = ', '.join(state.campos_faltantes) if state.campos_faltantes else 'informações específicas'
                state.recomendacao = (
                    f"❓ Solicite mais informações do usuário: {campos}. "
                    f"{state.resposta_rag[:100] if state.resposta_rag else ''}"
                )
                state.acao_sugerida = "Solicitar mais informações"
                
            else:  # ABRIR_CHAMADO
                state.recomendacao = (
                    f"🎫 Abra um chamado no sistema de Service Desk. "
                    f"Urgência: {state.urgencia}. "
                    "Motivo: Solicitação que requer processamento manual."
                )
                state.acao_sugerida = self._determinar_acao_chamado(state.urgencia)
            
            print(f"✅ Recomendação gerada: {state.acao_sugerida}")
            
        except Exception as e:
            state.erro = f"Erro ao gerar recomendação: {e}"
            print(f"❌ Erro ao gerar recomendação: {e}")
        
        return state
    
    def solicitar_mais_info(self, state: ServiceDeskState) -> ServiceDeskState:
        """
        Nó para solicitar mais informações do usuário.
        
        Args:
            state: Estado atual do grafo
            
        Returns:
            Estado atualizado com solicitação de informações
        """
        try:
            print("❓ Solicitando mais informações...")
            
            # Incrementa tentativas
            state.tentativas += 1
            
            # Gera mensagem de solicitação
            if state.campos_faltantes:
                campos = ', '.join(state.campos_faltantes)
                state.recomendacao = f"❓ Para melhor atendê-lo, preciso saber mais sobre: {campos}"
            else:
                state.recomendacao = "❓ Para melhor atendê-lo, preciso de mais informações específicas sobre sua solicitação."
            
            state.acao_sugerida = "Solicitar mais informações"
            
            # Verifica se excedeu o limite de tentativas
            if state.tentativas >= state.max_tentativas:
                state.recomendacao += " (Limite de tentativas atingido. Abrindo chamado.)"
                state.acao_sugerida = "Abrir chamado após limite de tentativas"
                state.precisa_mais_info = False
            
            print(f"✅ Solicitação de informações gerada (tentativa {state.tentativas})")
            
        except Exception as e:
            state.erro = f"Erro ao solicitar informações: {e}"
            print(f"❌ Erro ao solicitar informações: {e}")
        
        return state
    
    def finalizar_processamento(self, state: ServiceDeskState) -> ServiceDeskState:
        """
        Nó final: marca o processamento como finalizado.
        
        Args:
            state: Estado atual do grafo
            
        Returns:
            Estado finalizado
        """
        print("🏁 Finalizando processamento...")
        state.finalizado = True
        print("✅ Processamento finalizado!")
        return state
    
    def _determinar_acao_chamado(self, urgencia: str) -> str:
        """
        Determina a ação específica para abertura de chamado.
        
        Args:
            urgencia: Nível de urgência
            
        Returns:
            Ação sugerida para o chamado
        """
        if urgencia == "ALTA":
            return "Abrir chamado URGENTE"
        elif urgencia == "MEDIA":
            return "Abrir chamado normal"
        else:
            return "Abrir chamado de baixa prioridade"
