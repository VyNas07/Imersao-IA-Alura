"""
Agente inteligente de Service Desk que combina triagem e RAG.
"""
from typing import Dict, Optional
from src.chains import TriagemChain
from src.tools.rag_local import RAGSystemLocal
from src.models import TriagemOut


class ServiceDeskAgent:
    """
    Agente inteligente que combina triagem e RAG para processar solicitações.
    """
    
    def __init__(self):
        """Inicializa o agente."""
        self.triagem_chain = TriagemChain()
        self.rag_system = RAGSystemLocal()
        self.initialized = False
    
    def inicializar(self) -> None:
        """Inicializa o agente e seus sistemas."""
        if not self.initialized:
            print("🤖 Inicializando agente de Service Desk...")
            self.rag_system.inicializar()
            self.initialized = True
            print("✅ Agente inicializado com sucesso!")
    
    def processar_solicitacao(self, mensagem: str) -> Dict:
        """
        Processa uma solicitação completa usando triagem + RAG.
        
        Args:
            mensagem: Mensagem do usuário
            
        Returns:
            Dict com resultado completo da análise
        """
        if not self.initialized:
            self.inicializar()
        
        # 1. Triagem da mensagem
        resultado_triagem = self.triagem_chain.processar(mensagem)
        
        # 2. Resposta baseada na triagem
        resposta_rag = None
        documentos_relevantes = []
        
        if resultado_triagem['decisão'] in ['AUTO_RESOLVER', 'PEDIR_INFO']:
            # Busca resposta no RAG
            try:
                resultado_rag = self.rag_system.consultar(mensagem)
                resposta_rag = resultado_rag['resposta']
                documentos_relevantes = resultado_rag['documentos_relevantes']
            except Exception as e:
                resposta_rag = f"Erro ao consultar políticas: {e}"
        
        # 3. Gera recomendação final
        recomendacao = self._gerar_recomendacao(resultado_triagem, resposta_rag)
        
        return {
            'mensagem_original': mensagem,
            'triagem': resultado_triagem,
            'resposta_rag': resposta_rag,
            'documentos_relevantes': documentos_relevantes,
            'recomendacao': recomendacao,
            'acao_sugerida': self._determinar_acao(resultado_triagem)
        }
    
    def _gerar_recomendacao(self, triagem: Dict, resposta_rag: Optional[str]) -> str:
        """Gera uma recomendação baseada na triagem e resposta RAG."""
        decisao = triagem['decisão']
        urgencia = triagem['urgencia']
        
        if decisao == 'AUTO_RESOLVER':
            if resposta_rag:
                return f"✅ Esta solicitação pode ser respondida automaticamente. Resposta baseada nas políticas: {resposta_rag[:200]}..."
            else:
                return "✅ Esta solicitação pode ser respondida automaticamente com base nas políticas da empresa."
        
        elif decisao == 'PEDIR_INFO':
            campos = ', '.join(triagem['campos_faltantes']) if triagem['campos_faltantes'] else 'informações específicas'
            return f"❓ Solicite mais informações do usuário: {campos}. {resposta_rag[:100] if resposta_rag else ''}"
        
        else:  # ABRIR_CHAMADO
            return f"🎫 Abra um chamado no sistema de Service Desk. Urgência: {urgencia}. Motivo: Solicitação que requer processamento manual."
    
    def _determinar_acao(self, triagem: Dict) -> str:
        """Determina a ação sugerida baseada na triagem."""
        decisao = triagem['decisão']
        urgencia = triagem['urgencia']
        
        if decisao == 'AUTO_RESOLVER':
            return "Responder automaticamente"
        elif decisao == 'PEDIR_INFO':
            return "Solicitar mais informações"
        else:  # ABRIR_CHAMADO
            if urgencia == 'ALTA':
                return "Abrir chamado URGENTE"
            elif urgencia == 'MEDIA':
                return "Abrir chamado normal"
            else:
                return "Abrir chamado de baixa prioridade"
    
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
        
        return self.rag_system.consultar(pergunta)
    
    def classificar_mensagem(self, mensagem: str) -> Dict:
        """
        Classifica apenas a mensagem (triagem) sem RAG.
        
        Args:
            mensagem: Mensagem para classificar
            
        Returns:
            Dict com resultado da triagem
        """
        return self.triagem_chain.processar(mensagem)
