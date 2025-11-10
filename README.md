# Sistema de Gestão de Extratos Bancários - Ipixuna do Pará

Sistema completo para gerenciamento de extratos e documentos bancários com detecção automática de contas e tipos de documentos.

## Características Principais

### Upload Inteligente
- **Upload múltiplo** sem limite de arquivos
- **Detecção automática** de tipo de documento (Conciliação, Corrente, Poupança, Aplicação)
- **Identificação automática** da conta bancária por número e agência
- **Drag and drop** para facilitar o envio

### Organização por Fundos/Secretarias
- **PMIP** - Prefeitura Municipal de Ipixuna do Pará
- **CM** - Câmara Municipal
- **FMS** - Fundo Municipal de Saúde
- **FME** - Fundo Municipal de Educação
- **FMAS** - Fundo Municipal de Assistência Social
- **FMMA** - Fundo Municipal de Meio Ambiente
- **FUNDEB** - Fundo de Educação Básica
- **FMDCA** - Fundo Municipal dos Direitos da Criança e Adolescente

### Contas Pré-carregadas
- **300+ contas** bancárias já cadastradas
- Bancos: BB, CEF, BANPARA, BRADESCO, SICREDI
- Agrupadas por fundo e banco

### Gestão de Documentos
- 4 tipos de documentos: Conciliação Bancária, Conta Corrente, Poupança e Aplicação
- Extração automática de datas, valores e período
- Visualização organizada por conta
- Download individual de cada PDF

## Instalação

### Requisitos
- Python 3.7+
- pip

### Passo a Passo

1. **Baixe e descompacte o projeto**

2. **Abra o terminal na pasta do projeto**

3. **Crie um ambiente virtual**
\`\`\`bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
\`\`\`

4. **Instale as dependências**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

5. **Execute o sistema**
\`\`\`bash
python app.py
\`\`\`

6. **Acesse no navegador**
\`\`\`
http://localhost:5000
\`\`\`

## Como Usar

### 1. Upload de Documentos

1. Na página inicial, arraste e solte seus PDFs na área de upload
2. Ou clique em "Selecionar Arquivos" para escolher os PDFs
3. O sistema automaticamente:
   - Identifica o tipo de documento (Conciliação, Corrente, Poupança, Aplicação)
   - Encontra a conta bancária pelo número
   - Extrai as datas e valores
   - Vincula à conta correta

### 2. Visualizar Documentos

1. Encontre a conta desejada na lista (organizada por fundo e banco)
2. Clique em "Ver Docs" para ver todos os documentos da conta
3. Você verá:
   - Lista completa de documentos anexados
   - Tipo, período, mês/ano de referência
   - Valor total de cada documento
   - Opção de visualizar o PDF ou deletar

### 3. Configurar Conta

1. Clique em "Config" na conta desejada
2. Marque se a conta tem:
   - ✓ Poupança
   - ✓ Aplicação/Investimento
3. Isso ajuda a organizar melhor os documentos esperados

## Estrutura de Arquivos

\`\`\`
projeto/
├── app.py                      # Aplicação principal Flask
├── requirements.txt            # Dependências Python
├── README.md                   # Este arquivo
├── extratos_bancarios.db       # Banco de dados SQLite (criado automaticamente)
├── uploads/                    # PDFs enviados (criado automaticamente)
└── templates/
    ├── base.html              # Template base
    ├── index.html             # Página principal
    ├── ver_documentos.html    # Visualizar documentos
    └── editar_conta.html      # Configurar conta
\`\`\`

## Solução de Problemas

### Erro: "python não é reconhecido"
Use `python3` ao invés de `python` ou reinstale o Python marcando "Add to PATH"

### Erro ao instalar dependências
\`\`\`bash
python -m pip install --upgrade pip
pip install -r requirements.txt
\`\`\`

### Conta não encontrada no upload
Verifique se o número da conta no PDF corresponde exatamente ao número cadastrado

### PDF não detecta dados
Alguns PDFs escaneados (imagens) não têm texto extraível. Use PDFs com texto selecionável.

## Tecnologias Utilizadas

- **Flask** - Framework web Python
- **SQLite** - Banco de dados
- **pdfplumber** - Extração de dados de PDFs
- **PyPDF2** - Manipulação de PDFs

## Suporte

Para dúvidas ou problemas, verifique:
1. Este README
2. Os logs no terminal onde o sistema está rodando
3. As mensagens de erro na interface web
