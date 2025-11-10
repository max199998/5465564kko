# Solução para Problemas de Instalação

## Erro ao Instalar Pillow

Se você encontrou o erro `KeyError: '__version__'` ao tentar instalar o Pillow, siga estes passos:

### Solução Rápida

1. **Atualize o pip primeiro:**
\`\`\`bash
python -m pip install --upgrade pip
\`\`\`

2. **Instale as dependências atualizadas:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Se o erro persistir:

**Opção 1 - Instalar versão mais recente do Pillow:**
\`\`\`bash
pip install Pillow --upgrade
\`\`\`

**Opção 2 - Instalar sem versões fixas (mais flexível):**
\`\`\`bash
pip install Flask pdfplumber Werkzeug PyPDF2 Pillow
\`\`\`

**Opção 3 - Instalar um por vez:**
\`\`\`bash
pip install Flask==3.1.0
pip install pdfplumber==0.11.4
pip install Werkzeug==3.1.3
pip install PyPDF2==3.0.1
pip install Pillow
\`\`\`

## Outros Erros Comuns

### Erro: "python não é reconhecido"
Use `python3` ao invés de `python`:
\`\`\`bash
python3 -m pip install -r requirements.txt
\`\`\`

### Erro: "Microsoft Visual C++ is required"
O Pillow precisa de ferramentas de compilação no Windows:

1. Baixe e instale o **Build Tools for Visual Studio**:
   https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. Durante a instalação, marque **"Desktop development with C++"**

3. Ou instale apenas o Pillow pré-compilado:
\`\`\`bash
pip install --only-binary :all: Pillow
\`\`\`

### Erro: "Permission denied"
Execute o terminal como Administrador (Windows) ou use `sudo` (Mac/Linux):
\`\`\`bash
sudo pip install -r requirements.txt
\`\`\`

## Verificar se tudo foi instalado corretamente

Depois de instalar, verifique:
\`\`\`bash
pip list
\`\`\`

Você deve ver:
- Flask (3.1.0 ou superior)
- pdfplumber (0.11.4 ou superior)
- Werkzeug (3.1.3 ou superior)
- PyPDF2 (3.0.1 ou superior)
- Pillow (11.0.0 ou superior)

## Teste Rápido

Execute este comando para testar se tudo está funcionando:
\`\`\`bash
python -c "import flask, pdfplumber, PyPDF2, PIL; print('Tudo instalado corretamente!')"
\`\`\`

Se aparecer "Tudo instalado corretamente!", pode executar o sistema:
\`\`\`bash
python app.py
