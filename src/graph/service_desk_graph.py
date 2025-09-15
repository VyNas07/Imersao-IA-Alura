"""
Grafo LangGraph para orquestração do sistema de Service Desk.

Este módulo define o fluxo de trabalho do sistema usando LangGraph,
permitindo fluxos condicionais e reutilização de componentes.
"""
from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from .state import ServiceDeskState
from .nodes import ServiceDeskNodes


class ServiceDeskGraph:
    """
    Grafo LangGraph para orquestração do sistema de Service Desk.
    
    Define o fluxo de trabalho que combina triagem, RAG e geração
    de recomendações de forma condicional e inteligente.
    """
    
    def __init__(self):
        """Inicializa o grafo com os nós e fluxos necessários."""
        self.nodes = ServiceDeskNodes()
        self.graph = self._criar_grafo()
    
    def _criar_grafo(self) -> StateGraph:
        """
        Cria e configura o grafo LangGraph.
        
        Returns:
            Grafo compilado pronto para execução
        """
        # Cria o grafo com o estado definido
        graph = StateGraph(ServiceDeskState)
        
        # Adiciona os nós ao grafo
        graph.add_node("triagem", self.nodes.executar_triagem)
        graph.add_node("rag", self.nodes.executar_rag)
        graph.add_node("recomendacao", self.nodes.gerar_recomendacao)
        graph.add_node("solicitar_info", self.nodes.solicitar_mais_info)
        graph.add_node("finalizar", self.nodes.finalizar_processamento)
        
        # Define o ponto de entrada
        graph.set_entry_point("triagem")
        
        # Define as arestas condicionais
        graph.add_conditional_edges(
            "triagem",
            self._decidir_proximo_passo_apos_triagem,
            {
                "rag": "rag",
                "solicitar_info": "solicitar_info",
                "recomendacao": "recomendacao",
                "finalizar": "finalizar"
            }
        )
        
        # Fluxo após RAG
        graph.add_edge("rag", "recomendacao")
        
        # Fluxo após solicitar informações
        graph.add_conditional_edges(
            "solicitar_info",
            self._decidir_proximo_passo_apos_info,
            {
                "finalizar": "finalizar",
                "rag": "rag"
            }
        )
        
        # Fluxo após recomendação
        graph.add_edge("recomendacao", "finalizar")
        
        # Fluxo final
        graph.add_edge("finalizar", END)
        
        return graph.compile()
    
    def _decidir_proximo_passo_apos_triagem(self, state: ServiceDeskState) -> Literal["rag", "solicitar_info", "recomendacao", "finalizar"]:
        """
        Decide o próximo passo após a triagem baseado na decisão.
        
        Args:
            state: Estado atual do grafo
            
        Returns:
            Nome do próximo nó a ser executado
        """
        if state.erro:
            return "finalizar"
        
        if state.decisao == "AUTO_RESOLVER":
            return "rag"
        elif state.decisao == "PEDIR_INFO":
            return "solicitar_info"
        elif state.decisao == "ABRIR_CHAMADO":
            return "recomendacao"
        else:
            return "finalizar"
    
    def _decidir_proximo_passo_apos_info(self, state: ServiceDeskState) -> Literal["finalizar", "rag"]:
        """
        Decide o próximo passo após solicitar informações.
        
        Args:
            state: Estado atual do grafo
            
        Returns:
            Nome do próximo nó a ser executado
        """
        if state.erro:
            return "finalizar"
        
        # Se excedeu o limite de tentativas, finaliza
        if state.tentativas >= state.max_tentativas:
            return "finalizar"
        
        # Se ainda precisa de mais informações, pode tentar RAG com o que tem
        if state.precisa_mais_info and state.tentativas < state.max_tentativas:
            return "rag"
        
        return "finalizar"
    
    def processar(self, mensagem: str) -> ServiceDeskState:
        """
        Processa uma mensagem através do grafo.
        
        Args:
            mensagem: Mensagem do usuário para processar
            
        Returns:
            Estado final com resultado do processamento
        """
        # Cria o estado inicial
        estado_inicial = ServiceDeskState(
            mensagem_original=mensagem,
            tentativas=0,
            max_tentativas=3
        )
        
        # Executa o grafo
        resultado = self.graph.invoke(estado_inicial)
        
        return resultado
    
    def processar_com_historico(self, mensagem: str, historico: list = None) -> ServiceDeskState:
        """
        Processa uma mensagem considerando histórico de conversas.
        
        Args:
            mensagem: Mensagem atual do usuário
            historico: Lista de mensagens anteriores (para futuras implementações)
            
        Returns:
            Estado final com resultado do processamento
        """
        # Por enquanto, processa normalmente
        # Futuramente pode usar o histórico para melhorar o contexto
        return self.processar(mensagem)
    
    def obter_fluxo_executado(self, estado) -> list:
        """
        Retorna o fluxo de nós que foram executados.
        
        Args:
            estado: Estado final do processamento (dict ou ServiceDeskState)
            
        Returns:
            Lista com os nós executados
        """
        fluxo = ["triagem"]
        
        # Acessa decisão e tentativas dependendo do tipo
        if isinstance(estado, dict):
            decisao = estado.get('decisao')
            tentativas = estado.get('tentativas', 0)
            max_tentativas = estado.get('max_tentativas', 3)
        else:
            decisao = estado.decisao
            tentativas = estado.tentativas
            max_tentativas = estado.max_tentativas
        
        if decisao == "AUTO_RESOLVER":
            fluxo.extend(["rag", "recomendacao"])
        elif decisao == "PEDIR_INFO":
            fluxo.append("solicitar_info")
            if tentativas < max_tentativas:
                fluxo.extend(["rag", "recomendacao"])
        elif decisao == "ABRIR_CHAMADO":
            fluxo.append("recomendacao")
        
        fluxo.append("finalizar")
        return fluxo
    
    def obter_estatisticas(self, estado) -> dict:
        """
        Retorna estatísticas do processamento.
        
        Args:
            estado: Estado final do processamento (dict ou ServiceDeskState)
            
        Returns:
            Dicionário com estatísticas
        """
        # Se é um dicionário, acessa via get
        if isinstance(estado, dict):
            return {
                "decisao": estado.get('decisao'),
                "urgencia": estado.get('urgencia'),
                "tentativas": estado.get('tentativas', 0),
                "documentos_consultados": len(estado.get('documentos_relevantes', [])),
                "tem_erro": bool(estado.get('erro')),
                "fluxo_executado": self.obter_fluxo_executado(estado)
            }
        
        # Se é um objeto ServiceDeskState, acessa diretamente
        return {
            "decisao": estado.decisao,
            "urgencia": estado.urgencia,
            "tentativas": estado.tentativas,
            "documentos_consultados": len(estado.documentos_relevantes),
            "tem_erro": bool(estado.erro),
            "fluxo_executado": self.obter_fluxo_executado(estado)
        }
