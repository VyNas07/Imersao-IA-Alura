"""
Agente inteligente de Service Desk com LangGraph.

Este agente usa LangGraph para orquestrar o fluxo de processamento,
permitindo fluxos condicionais e reutilização de componentes.
"""
from typing import Dict, Optional
from src.graph import ServiceDeskGraph
from src.graph.state import ServiceDeskState


class ServiceDeskAgent:
    """
    Agente inteligente que usa LangGraph para orquestrar o processamento.
    
    Combina triagem, RAG e geração de recomendações através de um
    grafo de fluxo de trabalho condicional.
    """
    
    def __init__(self):
        """Inicializa o agente com o grafo LangGraph."""
        self.graph = ServiceDeskGraph()
        self.initialized = False
    
    def inicializar(self) -> None:
        """Inicializa o agente e seus sistemas."""
        if not self.initialized:
            print("🤖 Inicializando agente de Service Desk com LangGraph...")
            # O grafo é inicializado sob demanda quando necessário
            self.initialized = True
            print("✅ Agente inicializado com sucesso!")
    
    def processar_solicitacao(self, mensagem: str) -> Dict:
        """
        Processa uma solicitação usando o grafo LangGraph.
        
        Args:
            mensagem: Mensagem do usuário
            
        Returns:
            Dict com resultado completo da análise
        """
        if not self.initialized:
            self.inicializar()
        
        # Processa através do grafo LangGraph
        estado_final = self.graph.processar(mensagem)
        
        # Converte o estado para o formato esperado
        return self._converter_estado_para_dict(estado_final)
    
    def _converter_estado_para_dict(self, estado) -> Dict:
        """
        Converte o estado do grafo para o formato de dicionário esperado.
        
        Args:
            estado: Estado final do grafo LangGraph (pode ser dict ou ServiceDeskState)
            
        Returns:
            Dict com resultado no formato compatível
        """
        # Se o estado já é um dicionário, retorna diretamente
        if isinstance(estado, dict):
            return {
                'mensagem_original': estado.get('mensagem_original', ''),
                'triagem': estado.get('triagem'),
                'resposta_rag': estado.get('resposta_rag'),
                'documentos_relevantes': estado.get('documentos_relevantes', []),
                'recomendacao': estado.get('recomendacao'),
                'acao_sugerida': estado.get('acao_sugerida'),
                'erro': estado.get('erro'),
                'finalizado': estado.get('finalizado', False),
                'tentativas': estado.get('tentativas', 0),
                'estatisticas': self.graph.obter_estatisticas(estado)
            }
        
        # Se é um objeto ServiceDeskState, converte
        return {
            'mensagem_original': estado.mensagem_original,
            'triagem': estado.triagem,
            'resposta_rag': estado.resposta_rag,
            'documentos_relevantes': estado.documentos_relevantes,
            'recomendacao': estado.recomendacao,
            'acao_sugerida': estado.acao_sugerida,
            'erro': estado.erro,
            'finalizado': estado.finalizado,
            'tentativas': estado.tentativas,
            'estatisticas': self.graph.obter_estatisticas(estado)
        }
    
    def processar_com_historico(self, mensagem: str, historico: list = None) -> Dict:
        """
        Processa uma mensagem considerando histórico de conversas.
        
        Args:
            mensagem: Mensagem atual do usuário
            historico: Lista de mensagens anteriores
            
        Returns:
            Dict com resultado completo da análise
        """
        if not self.initialized:
            self.inicializar()
        
        # Processa através do grafo com histórico
        estado_final = self.graph.processar_com_historico(mensagem, historico)
        
        # Converte o estado para o formato esperado
        return self._converter_estado_para_dict(estado_final)
    
    def obter_estatisticas(self, mensagem: str) -> Dict:
        """
        Obtém estatísticas do processamento de uma mensagem.
        
        Args:
            mensagem: Mensagem para processar
            
        Returns:
            Dict com estatísticas do processamento
        """
        if not self.initialized:
            self.inicializar()
        
        estado_final = self.graph.processar(mensagem)
        return self.graph.obter_estatisticas(estado_final)
    
    def consultar_politicas(self, pergunta: str) -> Dict:
        """
        Consulta apenas as políticas (RAG) sem triagem.
        
        Args:
            pergunta: Pergunta sobre políticas
            
        Returns:
            Dict com resposta e documentos relevantes
        """
        if not self.initialized:
            self.inicializar()
        
        # Usa o sistema RAG diretamente do grafo
        self.graph.nodes._inicializar_rag()
        return self.graph.nodes.rag_system.consultar(pergunta)
    
    def classificar_mensagem(self, mensagem: str) -> Dict:
        """
        Classifica apenas a mensagem (triagem) sem RAG.
        
        Args:
            mensagem: Mensagem para classificar
            
        Returns:
            Dict com resultado da triagem
        """
        if not self.initialized:
            self.inicializar()
        
        # Usa a chain de triagem diretamente do grafo
        return self.graph.nodes.triagem_chain.processar(mensagem)
