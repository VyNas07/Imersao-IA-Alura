# 🏢 Sistema de Service Desk com IA - Como Usar

## 🚀 Execução Rápida

### Opção 1: Interface Simples (Recomendada)
```bash
python run.py
```

### Opção 2: Interface Completa com Menu
```bash
python cli.py
```

## 📋 Pré-requisitos

1. **Configurar API Key**:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione: `GOOGLE_API_KEY=sua_chave_do_google_gemini`

2. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **PDFs de Políticas**:
   - Coloque os PDFs na pasta `Pdf_Imersao_IA/`
   - O sistema carregará automaticamente todos os PDFs

## 🎯 Como Funciona

### Sistema Integrado (run.py)
- **Entrada**: Digite sua pergunta ou solicitação
- **Processamento**: 
  1. Sistema de triagem classifica a mensagem
  2. Sistema RAG busca resposta nas políticas
  3. Gera recomendação final
- **Saída**: Decisão, urgência, resposta e ação sugerida

### Exemplos de Uso

#### Perguntas sobre Políticas
```
👤 Você: Qual é a política de home office?
🤖 Sistema: 
📊 TRIAGEM: AUTO_RESOLVER - BAIXA
💡 RESPOSTA: A empresa adota modelo híbrido: mínimo de 2 dias presenciais...
🎯 RECOMENDAÇÃO: ✅ Esta solicitação pode ser respondida automaticamente
⚡ AÇÃO SUGERIDA: Responder automaticamente
```

#### Solicitações que Precisam de Chamado
```
👤 Você: Minha máquina quebrou e preciso de uma nova urgente
🤖 Sistema:
📊 TRIAGEM: ABRIR_CHAMADO - ALTA
🎯 RECOMENDAÇÃO: 🎫 Abra um chamado no sistema de Service Desk
⚡ AÇÃO SUGERIDA: Abrir chamado URGENTE
```

#### Mensagens que Precisam de Mais Informações
```
👤 Você: Preciso de ajuda com uma política
🤖 Sistema:
📊 TRIAGEM: PEDIR_INFO - MEDIA
🎯 RECOMENDAÇÃO: ❓ Solicite mais informações do usuário
⚡ AÇÃO SUGERIDA: Solicitar mais informações
```

## 🔧 Funcionalidades

### Sistema de Triagem
- **AUTO_RESOLVER**: Perguntas que podem ser respondidas automaticamente
- **PEDIR_INFO**: Mensagens que precisam de mais informações
- **ABRIR_CHAMADO**: Solicitações que requerem abertura de chamado

### Sistema RAG
- Busca inteligente em documentos PDF
- Respostas baseadas nas políticas da empresa
- Citação de documentos relevantes

### Níveis de Urgência
- **BAIXA**: Questões rotineiras
- **MEDIA**: Questões importantes
- **ALTA**: Questões urgentes

## 🛠️ Comandos Úteis

### Para Sair
- Digite `sair`, `exit`, `quit` ou pressione `Ctrl+C`

### Para Testar
```bash
# Testar apenas RAG
python test_rag_local.py

# Testar sistema de triagem
python -m src.main
```

## 📁 Estrutura do Projeto

```
├── run.py              # Execução principal (recomendada)
├── cli.py              # Interface completa com menu
├── src/
│   ├── agents/         # Agentes inteligentes
│   ├── chains/         # Cadeias de processamento
│   ├── tools/          # Ferramentas (RAG)
│   └── models.py       # Modelos de dados
├── Pdf_Imersao_IA/     # PDFs de políticas
└── requirements.txt    # Dependências
```

## 🚨 Solução de Problemas

### Erro de API Key
```
❌ Erro: GOOGLE_API_KEY não configurada
```
**Solução**: Crie arquivo `.env` com sua chave do Google Gemini

### Erro de PDFs
```
❌ Pasta não encontrada: Pdf_Imersao_IA
```
**Solução**: Crie a pasta e adicione os PDFs de políticas

### Erro de Dependências
```
❌ ModuleNotFoundError
```
**Solução**: Execute `pip install -r requirements.txt`

## 🎉 Pronto para Usar!

O sistema está configurado para funcionar localmente no terminal. Basta executar `python run.py` e começar a fazer perguntas!
