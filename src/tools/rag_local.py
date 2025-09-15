"""
Sistema RAG alternativo usando embeddings locais (sem limite de quota).
"""
import os
from pathlib import Path
from typing import List, Dict
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from src.config.settings import GOOGLE_API_KEY


class RAGSystemLocal:
    """
    Sistema RAG usando embeddings locais (HuggingFace) para evitar limites de quota.
    """
    
    def __init__(self, pdf_folder: str = "Pdf_Imersao_IA"):
        """
        Inicializa o sistema RAG com embeddings locais.
        
        Args:
            pdf_folder: Caminho para a pasta com os PDFs
        """
        self.pdf_folder = Path(pdf_folder)
        self.docs = []
        self.vectorstore = None
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=GOOGLE_API_KEY,
        )
        # Usa embeddings locais do HuggingFace
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
    def carregar_documentos(self) -> None:
        """Carrega todos os PDFs da pasta especificada."""
        print("📚 Carregando documentos PDF...")
        
        if not self.pdf_folder.exists():
            raise FileNotFoundError(f"Pasta não encontrada: {self.pdf_folder}")
        
        for pdf_file in self.pdf_folder.glob("*.pdf"):
            try:
                loader = PyMuPDFLoader(str(pdf_file))
                docs = loader.load()
                self.docs.extend(docs)
                print(f"✅ Arquivo carregado: {pdf_file.name}")
            except Exception as e:
                print(f"❌ Erro ao carregar {pdf_file.name}: {e}")
        
        print(f"📊 Total de documentos carregados: {len(self.docs)}")
    
    def processar_documentos(self) -> None:
        """Processa os documentos e cria o índice vetorial."""
        if not self.docs:
            raise ValueError("Nenhum documento carregado. Execute carregar_documentos() primeiro.")
        
        print("🔧 Processando documentos...")
        
        # Divide os documentos em chunks menores
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        splits = text_splitter.split_documents(self.docs)
        print(f"📄 Documentos divididos em {len(splits)} chunks")
        
        # Cria o índice vetorial com embeddings locais
        print("🔍 Criando índice vetorial com embeddings locais...")
        self.vectorstore = FAISS.from_documents(splits, self.embeddings)
        print("✅ Índice vetorial criado com sucesso!")
    
    def consultar(self, pergunta: str, k: int = 3) -> Dict:
        """
        Consulta o sistema RAG com uma pergunta.
        
        Args:
            pergunta: Pergunta do usuário
            k: Número de documentos relevantes para recuperar
            
        Returns:
            Dict com a resposta e documentos relevantes
        """
        if not self.vectorstore:
            raise ValueError("Sistema não inicializado. Execute carregar_documentos() e processar_documentos() primeiro.")
        
        # Busca documentos relevantes
        docs_relevantes = self.vectorstore.similarity_search(pergunta, k=k)
        
        # Cria o contexto a partir dos documentos
        contexto = "\n\n".join([doc.page_content for doc in docs_relevantes])
        
        # Prompt para o LLM
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um assistente especializado em políticas da empresa Carraro Desenvolvimento.
            
            Use APENAS as informações fornecidas no contexto abaixo para responder à pergunta.
            Se a informação não estiver no contexto, diga que não tem essa informação disponível.
            
            Seja claro, objetivo e cite a política específica quando possível.
            
            Contexto:
            {contexto}"""),
            ("human", "{pergunta}")
        ])
        
        # Gera a resposta
        chain = prompt | self.llm
        resposta = chain.invoke({
            "contexto": contexto,
            "pergunta": pergunta
        })
        
        return {
            "resposta": resposta.content,
            "documentos_relevantes": [
                {
                    "fonte": doc.metadata.get("source", "Desconhecida"),
                    "conteudo": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                }
                for doc in docs_relevantes
            ]
        }
    
    def inicializar(self) -> None:
        """Inicializa o sistema RAG completo."""
        self.carregar_documentos()
        self.processar_documentos()


# Função de conveniência para uso rápido
def criar_sistema_rag_local() -> RAGSystemLocal:
    """Cria e inicializa um sistema RAG com embeddings locais."""
    sistema = RAGSystemLocal()
    sistema.inicializar()
    return sistema
