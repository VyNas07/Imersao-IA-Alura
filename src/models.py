"""
Modelos Pydantic para validação de dados do sistema de triagem.
"""
from pydantic import BaseModel, Field
from typing import List, Literal


class TriagemOut(BaseModel):
    """
    Modelo de saída para o sistema de triagem de Service Desk.
    
    Define a estrutura de resposta para classificação de mensagens
    de usuários do Service Desk.
    """
    decisão: Literal["AUTO_RESOLVER", "PEDIR_INFO", "ABRIR_CHAMADO"]
    urgencia: Literal["BAIXA", "MEDIA", "ALTA"]
    campos_faltantes: List[str] = Field(default_factory=list)
