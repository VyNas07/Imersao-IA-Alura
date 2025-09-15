"""
Modelo de estado para o grafo de Service Desk.

Define a estrutura de dados que é compartilhada entre todos os nós
do grafo LangGraph durante a execução.
"""
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field


class ServiceDeskState(BaseModel):
    """
    Estado compartilhado do grafo de Service Desk.
    
    Este estado é passado entre todos os nós do grafo e contém
    todas as informações necessárias para o processamento.
    """
    
    # Entrada do usuário
    mensagem_original: str = Field(description="Mensagem original do usuário")
    
    # Resultado da triagem
    triagem: Optional[Dict] = Field(default=None, description="Resultado da triagem")
    decisao: Optional[Literal["AUTO_RESOLVER", "PEDIR_INFO", "ABRIR_CHAMADO"]] = Field(
        default=None, description="Decisão da triagem"
    )
    urgencia: Optional[Literal["BAIXA", "MEDIA", "ALTA"]] = Field(
        default=None, description="Nível de urgência"
    )
    campos_faltantes: List[str] = Field(
        default_factory=list, description="Campos que faltam informações"
    )
    
    # Resultado do RAG
    resposta_rag: Optional[str] = Field(default=None, description="Resposta do sistema RAG")
    documentos_relevantes: List[Dict] = Field(
        default_factory=list, description="Documentos consultados pelo RAG"
    )
    
    # Recomendações e ações
    recomendacao: Optional[str] = Field(default=None, description="Recomendação final")
    acao_sugerida: Optional[str] = Field(default=None, description="Ação sugerida")
    
    # Controle de fluxo
    precisa_mais_info: bool = Field(default=False, description="Se precisa de mais informações")
    tentativas: int = Field(default=0, description="Número de tentativas de obter informações")
    max_tentativas: int = Field(default=3, description="Máximo de tentativas permitidas")
    
    # Metadados
    erro: Optional[str] = Field(default=None, description="Mensagem de erro se houver")
    finalizado: bool = Field(default=False, description="Se o processamento foi finalizado")
    
    class Config:
        """Configuração do modelo Pydantic."""
        arbitrary_types_allowed = True
        validate_assignment = True
