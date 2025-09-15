# 🏢 Sistema de Service Desk com IA

Sistema inteligente que combina **triagem automática** e **RAG (Retrieval-Augmented Generation)** para processar solicitações de usuários e consultar políticas da empresa.

## 🚀 Execução

```bash
# Interface simples (recomendada)
python run.py

# Interface completa com menu
python cli.py
```

## ⚙️ Configuração

1. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar API Key** (criar arquivo `.env`):
   ```env
   GOOGLE_API_KEY=sua_chave_do_google_gemini
   ```

3. **Adicionar PDFs** na pasta `Pdf_Imersao_IA/`

## 🎯 Funcionalidades

### Sistema de Triagem
- **AUTO_RESOLVER**: Perguntas que podem ser respondidas automaticamente
- **PEDIR_INFO**: Mensagens que precisam de mais informações
- **ABRIR_CHAMADO**: Solicitações que requerem abertura de chamado

### Sistema RAG
- Busca semântica em documentos PDF
- Respostas baseadas nas políticas da empresa
- Citação de documentos relevantes

### Agente Inteligente
- Combina triagem + RAG automaticamente
- Gera recomendações baseadas na análise
- Sugere ações apropriadas

## 🧪 Testes

```bash
# Testar sistema de triagem
python -m src.main

# Testar sistema RAG
python test_rag_local.py
```

## 🏗️ Arquitetura

```
src/
├── agents/              # Agente principal que orquestra o fluxo
├── chains/              # Sistema de triagem com LangChain
├── tools/               # Sistema RAG com embeddings locais
├── config/              # Gerenciamento de configurações
└── models.py            # Modelos Pydantic para validação
```

## 🛠️ Tecnologias

- **Python 3.12+** - Linguagem principal
- **LangChain** - Framework para aplicações com LLM
- **LangGraph** - Orquestração de agentes com grafos
- **Google Gemini** - Modelo de linguagem
- **FAISS** - Indexação vetorial
- **Pydantic** - Validação de dados
- **HuggingFace** - Embeddings locais

> 📖 **Detalhes técnicos**: [TECNOLOGIAS.md](TECNOLOGIAS.md)

## 📊 Exemplo de Uso

```
👤 Você: Qual é a política de home office?

📊 TRIAGEM:
   Decisão: AUTO_RESOLVER
   Urgência: BAIXA

💡 RESPOSTA:
   A empresa adota modelo híbrido: mínimo de 2 dias presenciais por semana...

🎯 RECOMENDAÇÃO:
   ✅ Esta solicitação pode ser respondida automaticamente

⚡ AÇÃO SUGERIDA: Responder automaticamente
```

## 🚨 Solução de Problemas

**Erro de API Key**: Verifique se o arquivo `.env` está configurado corretamente
**Erro de PDFs**: Certifique-se de que os PDFs estão na pasta `Pdf_Imersao_IA/`
**Erro de dependências**: Execute `pip install -r requirements.txt`
