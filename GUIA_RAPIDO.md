# 🚀 Guia Rápido - Sistema de Extratos

## Instalação em 3 Passos

\`\`\`bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 3. Instalar e executar
pip install -r requirements.txt
python app.py
\`\`\`

Acesse: http://localhost:5000

## Como Usar

### Upload de Documentos
1. **Arraste** PDFs para a área de upload OU
2. **Clique** em "Selecionar Arquivos"
3. **Aguarde** o processamento automático
4. **Pronto!** Os documentos são organizados automaticamente

### Ver Documentos
1. Localize a conta na lista
2. Clique em "Ver Documentos"
3. Visualize ou delete documentos

### Configurar Conta
1. Clique em "Configurar" na conta
2. Marque se tem Poupança/Aplicação
3. Salve as configurações

## O que o Sistema Faz Automaticamente

- Identifica o tipo de documento  
- Encontra a conta bancária  
- Extrai datas e valores  
- Organiza tudo para você  

## Tipos de Documentos Detectados

🔵 **Conciliação Bancária**  
🟢 **Conta Corrente**  
🟣 **Conta Poupança**  
🟠 **Conta de Aplicação**

## Atalhos Úteis

- **Ctrl + Clique** - Selecionar múltiplos arquivos
- **Shift + Clique** - Selecionar intervalo de arquivos
- **Arrastar múltiplos** - Upload em lote

## Estrutura de Pastas

\`\`\`
projeto/
├── app.py              # Sistema principal
├── uploads/            # PDFs salvos
├── extratos_bancarios.db  # Banco de dados
└── templates/          # Interface web
\`\`\`

## Backup

Copie estas pastas regularmente:
- `uploads/` - Todos os PDFs
- `extratos_bancarios.db` - Banco de dados

## Problemas Comuns

**"Conta não encontrada"**  
→ Verifique se o número da conta está correto no sistema

**"Erro ao ler PDF"**  
→ PDF pode estar protegido ou corrompido

**PDFs não detectados**  
→ Certifique-se que o PDF contém texto (não é imagem)

## Suporte

- Veja o **README.md** para instruções detalhadas
- Confira os logs no terminal do servidor
- Verifique as mensagens de erro na tela

---

Sistema de Extratos Bancários v2.0  
Ipixuna do Pará - 2025
