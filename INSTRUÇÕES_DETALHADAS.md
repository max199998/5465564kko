# 📘 INSTRUÇÕES DETALHADAS - Sistema de Extratos Bancários

## 🎯 VISÃO GERAL DO SISTEMA

Este sistema foi desenvolvido especificamente para gerenciar documentos bancários da **Prefeitura Municipal de Ipixuna do Pará**, incluindo:

- ✅ Conciliações Bancárias
- 📊 Extratos de Conta Corrente
- 💰 Extratos de Conta Poupança
- 📈 Extratos de Conta de Aplicação

O sistema já vem com **180+ contas bancárias pré-cadastradas** de diversos bancos (BB, BANPARÁ, Caixa, etc).

---

## 🔥 FUNCIONALIDADES PRINCIPAIS

### 1. DOCUMENTOS (Página Principal)

**O que você pode fazer:**
- ✅ Fazer upload de PDFs de documentos bancários
- ✅ Sistema extrai automaticamente dados do PDF
- ✅ Filtrar documentos por conta, tipo, mês e ano
- ✅ Visualizar PDF no navegador
- ✅ Deletar documentos

**Como usar:**

#### Upload de Documento
1. Selecione a **Conta Bancária** do dropdown (ex: "001 - Banco do Brasil | Ag: 4876-3 | Conta: 5076-8")
2. Escolha o **Tipo de Documento**:
   - 📊 Conta Corrente
   - 💰 Conta Poupança
   - 📈 Conta de Aplicação
   - ✅ Conciliação Bancária
3. Clique em **"Escolher arquivo"** e selecione o PDF
4. (Opcional) Adicione observações
5. Clique em **📤 Enviar Documento**

**O sistema automaticamente:**
- Extrai as datas de início e fim
- Identifica o mês/ano de referência (ex: AGOSTO/2025)
- Captura o valor total
- Salva o arquivo com nome único

#### Filtrar Documentos
Use os filtros para encontrar documentos específicos:
- **Por Conta**: Veja apenas documentos de uma conta
- **Por Tipo**: Filtre Corrente, Poupança, Aplicação ou Conciliação
- **Por Mês**: Selecione mês específico
- **Por Ano**: Selecione ano específico

Combine múltiplos filtros para busca precisa!

---

### 2. CONTAS

**O que você pode fazer:**
- ✅ Adicionar novas contas bancárias
- ✅ Editar informações de contas existentes
- ✅ Ativar/Desativar contas
- ✅ Deletar contas (sem documentos vinculados)
- ✅ Adicionar novos bancos ao sistema
- ✅ Ver quantos documentos cada conta possui

**Como usar:**

#### Adicionar Nova Conta
1. Vá para **💳 Contas**
2. Preencha o formulário:
   - **Banco**: Escolha da lista (001-BB, 037-BANPARÁ, 104-Caixa, etc)
   - **Agência**: Digite a agência (ex: 4876-3)
   - **Número da Conta**: Digite o número (ex: 5.076-8)
   - **Descrição**: Nome/finalidade da conta (ex: PMIPX/PA-PG. PESSOAL)
3. Clique **➕ Adicionar Conta**

#### Editar Conta
1. Na tabela de contas, localize a conta
2. Clique em **✏️ Editar**
3. Um modal abrirá com os dados atuais
4. Modifique o que desejar
5. Clique **💾 Salvar Alterações**

#### Desativar Conta (Sem deletar documentos)
- Use quando a conta não está mais em uso mas quer manter o histórico
- Clique em **⏸ Desativar**
- Contas inativas não aparecem nos formulários de upload
- Para reativar, clique **▶️ Ativar**

#### Deletar Conta Permanentemente
⚠️ **ATENÇÃO**: Só funciona se a conta NÃO tiver documentos vinculados
- Se tiver documentos, delete-os primeiro
- Clique em **🗑 Deletar**
- Confirme a ação

#### Adicionar Novo Banco
Se o banco não existe na lista:
1. Role até **🏦 Adicionar Novo Banco**
2. Digite o **Código** (ex: 341 para Itaú)
3. Digite o **Nome Completo** (ex: Banco Itaú Unibanco S.A.)
4. Clique **➕ Adicionar Banco**

---

### 3. UNIR DOCUMENTOS (Recurso Especial!)

**Para que serve:**
Você pode **selecionar múltiplos documentos** de uma conta e baixar todos unidos em **um único PDF**!

**Casos de Uso Reais:**

1️⃣ **Documentação Mensal Completa**
   - Selecione: Conciliação + Conta Corrente + Poupança de Agosto/2025
   - Resultado: 1 PDF com os 3 documentos

2️⃣ **Relatório de Aplicações Trimestral**
   - Selecione: Todas as Aplicações de Jan, Fev e Mar
   - Resultado: 1 PDF consolidado

3️⃣ **Arquivo Anual**
   - Selecione: Todos os documentos do ano
   - Resultado: 1 PDF completo para arquivo

**Como usar:**

1. Vá para **📎 Unir Documentos**
2. **Passo 1**: Selecione a conta no dropdown
3. **Passo 2**: O sistema mostrará todos os documentos desta conta, organizados por mês/ano
4. **Selecione os documentos**:
   - ✅ Marque individualmente cada documento que deseja
   - OU clique em **"Selecionar Todos deste Período"** para marcar um mês inteiro
   - OU clique em **✅ Selecionar Todos** para marcar tudo
5. O contador mostrará quantos documentos estão selecionados
6. Clique em **📥 Baixar Documentos Selecionados em PDF Único**
7. O arquivo será baixado automaticamente

**Organização Automática:**
O sistema organiza os documentos no PDF final por:
1. Ano (mais recente primeiro)
2. Mês
3. Tipo de documento

---

## 📊 ESTRUTURA DAS CONTAS PRÉ-CARREGADAS

O sistema já vem com contas do arquivo CONTAS.txt, incluindo:

### Banco do Brasil (001)
- Múltiplas contas para diferentes finalidades
- FMS (Fundo Municipal de Saúde)
- FME (Fundo Municipal de Educação)
- FUNDEB
- Programas federais (PNAE, PNTE, etc)

### Banco do Estado do Pará - BANPARÁ (037)
- Contas convênio
- Pavimentação
- Obras públicas
- ICMS

### Caixa Econômica Federal (104)
- Contas de saúde
- Investimentos
- Programas sociais

### Outros Bancos
- Bradesco (237)
- Sicredi (748)

**Total: 180+ contas já cadastradas!**

---

## 🎨 TIPOS DE DOCUMENTOS

### 📊 Conta Corrente
- Extrato de movimentação da conta corrente
- Mostra entradas, saídas e saldo
- Geralmente mensal

### 💰 Conta Poupança
- Extrato da conta poupança
- Mostra aplicações, resgates e rendimentos
- Pode ser mensal ou sob demanda

### 📈 Conta de Aplicação
- Extrato de investimentos
- BB RF CP Automático (Renda Fixa Curto Prazo)
- Mostra rentabilidade, IR, IOF
- Geralmente mensal

### ✅ Conciliação Bancária
- Documento contábil
- Compara saldo bancário vs contábil
- Inclui pendências e ajustes
- Geralmente mensal (fim do mês)

---

## 💡 DICAS E BOAS PRÁTICAS

### Upload de Documentos
1. ✅ **Sempre selecione a conta correta** antes do upload
2. ✅ **Escolha o tipo de documento correto** para facilitar filtros
3. ✅ Use **observações** para notas importantes (ex: "Verificar pendência item X")
4. ✅ Faça upload assim que receber os documentos
5. ✅ Mantenha uma rotina mensal de uploads

### Organização
1. 📁 **Cadastre contas antes** de fazer uploads massivos
2. 📁 Use **descrições claras** nas contas (ex: "FUNDEB 60%" ao invés de "Conta 1")
3. 📁 **Desative contas antigas** ao invés de deletar
4. 📁 Use os **filtros** para encontrar documentos rapidamente

### Unir Documentos
1. 📎 **Planeje o que precisa** antes de selecionar
2. 📎 Para arquivo mensal: Una Conciliação + Corrente + Poupança
3. 📎 Para relatórios: Una apenas o tipo específico (ex: só Aplicações)
4. 📎 Nomeie os PDFs baixados adequadamente para fácil identificação

---

## ⚙️ CONFIGURAÇÕES AVANÇADAS

### Limite de Upload
- **Tamanho máximo**: 50MB por arquivo
- Se precisar mais, edite `MAX_CONTENT_LENGTH` no app.py

### Banco de Dados
- **Arquivo**: `extratos_bancarios.db`
- **Tipo**: SQLite (arquivo único)
- **Backup**: Basta copiar o arquivo .db

### Arquivos PDF
- **Pasta**: `uploads/`
- **Nomeação**: Data_Hora + Nome_Original
- **Backup**: Copie toda a pasta uploads/

---

## 🔍 EXTRAÇÃO AUTOMÁTICA - Como Funciona

O sistema usa a biblioteca **pdfplumber** para ler o texto do PDF:

### O que o sistema procura:

1. **Datas**:
   - Padrões: dd/mm/yyyy ou dd-mm-yyyy
   - Palavras-chave: "período", "de", "até", "data inicial", "data final"

2. **Valores**:
   - Formato: R$ 1.234,56 ou 1.234,56
   - Palavras-chave: "saldo", "total", "valor"

3. **Mês/Ano**:
   - Formato: AGOSTO/2025
   - Palavras-chave: "mês/ano", "referência"

4. **Tipo**:
   - Detecta palavras: "cartão", "poupança", "corrente", "aplicação"

### Limitações:
- PDFs escaneados (imagens) não funcionam
- Formatação muito complexa pode falhar
- Valores padrão são usados se não encontrar

---

## 🆘 RESOLUÇÃO DE PROBLEMAS

### Problema: "Conta não aparece no upload"
**Solução**: A conta pode estar desativada. Vá em Contas e ative-a.

### Problema: "Erro ao fazer upload"
**Solução**: 
1. Verifique se é um PDF válido
2. Verifique o tamanho (máx 50MB)
3. Selecione conta e tipo

### Problema: "Dados extraídos incorretos"
**Solução**: 
- Normal para PDFs complexos
- Os documentos ainda são salvos corretamente
- Futuras versões permitirão edição manual

### Problema: "Não consigo deletar conta"
**Solução**: 
- Delete primeiro os documentos vinculados
- Ou use "Desativar" ao invés de deletar

---

## 📈 RELATÓRIOS E ANÁLISES

### Quantos documentos por conta?
- Vá em **💳 Contas**
- A coluna "Docs" mostra o total de documentos

### Documentos de um período?
- Vá em **📄 Documentos**
- Use filtros de Mês + Ano

### Documentos de uma conta específica?
- Use o filtro "Conta" na página Documentos

---

## 🎓 TREINAMENTO RÁPIDO

### Para Iniciantes (5 minutos):
1. Abra o sistema (localhost:5000)
2. Vá em **💳 Contas** - veja as contas já cadastradas
3. Vá em **📄 Documentos** - faça upload de 1 PDF
4. Veja o documento aparecer na lista

### Para Usuários Intermediários (15 minutos):
1. Adicione uma nova conta
2. Faça upload de 3 documentos diferentes
3. Use os filtros para encontrá-los
4. Vá em **📎 Unir Documentos** e crie um PDF unificado

### Para Usuários Avançados (30 minutos):
1. Adicione um novo banco
2. Adicione múltiplas contas deste banco
3. Faça upload em massa de documentos
4. Experimente diferentes combinações de filtros
5. Crie PDFs unificados por tipo e período
6. Desative contas antigas

---

## 📞 CONTATO E SUPORTE

Este sistema foi desenvolvido especialmente para a gestão de documentos bancários.

Para melhorias ou novas funcionalidades, considere:
- Exportação para Excel
- Gráficos de valores por período
- Notificações de documentos pendentes
- Busca por texto dentro dos PDFs
- Múltiplos usuários com permissões

---

**🎉 Sistema pronto para uso! Boa gestão de documentos!**
