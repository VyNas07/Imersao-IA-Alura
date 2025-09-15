# 🛠️ Tecnologias e Arquitetura

## Stack Tecnológico

### Backend
- **Python 3.12+** - Linguagem principal
- **LangChain** - Framework para aplicações com LLM
- **Pydantic** - Validação de dados e modelos
- **FAISS** - Indexação vetorial para busca semântica

### IA e ML
- **Google Gemini 1.5 Flash** - Modelo de linguagem principal
- **HuggingFace Embeddings** - Embeddings locais (sentence-transformers)
- **PyMuPDF** - Processamento de documentos PDF

### Configuração
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Pathlib** - Manipulação de caminhos

## Arquitetura

### Padrão de Design
- **Agent Pattern** - Agente central que orquestra o fluxo
- **Chain of Responsibility** - Cadeias de processamento
- **Repository Pattern** - Abstração de acesso a dados

### Fluxo de Dados
```
Usuário → Agente → Triagem → RAG → Recomendação → Resposta
```

### Componentes

#### 1. ServiceDeskAgent
- Orquestra todo o fluxo de processamento
- Combina triagem e RAG
- Gera recomendações finais

#### 2. TriagemChain
- Classifica mensagens usando LLM estruturado
- Valida saída com Pydantic
- Define regras de negócio

#### 3. RAGSystem
- Carrega e processa documentos PDF
- Cria índice vetorial com FAISS
- Realiza busca semântica

## Decisões Técnicas

### Por que LangChain?
- Framework maduro para aplicações com LLM
- Integração nativa com múltiplos provedores
- Suporte a structured output

### Por que FAISS?
- Indexação vetorial eficiente
- Suporte a busca semântica
- Integração com LangChain

### Por que Embeddings Locais?
- Evita limites de quota de APIs
- Funciona offline após download inicial
- Controle total sobre o processamento

### Por que Pydantic?
- Validação automática de dados
- Type hints nativos
- Integração com LangChain structured output

## Performance

- **Inicialização**: ~10-15 segundos (primeira vez)
- **Resposta**: ~2-5 segundos por consulta
- **Memória**: ~500MB (com embeddings locais)
- **Documentos**: Suporte a múltiplos PDFs

## Extensibilidade

O sistema foi projetado para ser facilmente extensível:

- **Novos tipos de documentos**: Implementar novos loaders
- **Novas categorias de triagem**: Atualizar modelos Pydantic
- **Novos agentes**: Seguir padrão estabelecido
- **Novas interfaces**: API REST, Web, etc.
