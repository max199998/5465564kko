from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, send_file, jsonify
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import pdfplumber
import re
from PyPDF2 import PdfMerger
import io
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-ipixuna-2025'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB para upload múltiplo

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def conectar_db():
    conn = sqlite3.connect('extratos_bancarios.db')
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_db():
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Criar tabela Bancos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bancos (
        id_banco INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_banco TEXT NOT NULL,
        nome_banco TEXT NOT NULL
    )
    ''')
    
    # Criar tabela Contas com flags para poupança e aplicação
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Contas (
        id_conta INTEGER PRIMARY KEY AUTOINCREMENT,
        fundo TEXT NOT NULL,
        banco TEXT NOT NULL,
        numero_conta TEXT NOT NULL,
        agencia TEXT DEFAULT '4876',
        tem_poupanca INTEGER DEFAULT 0,
        tem_aplicacao INTEGER DEFAULT 0,
        ativa INTEGER DEFAULT 1,
        UNIQUE(fundo, banco, numero_conta)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Documentos (
        id_documento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_conta INTEGER NOT NULL,
        tipo_documento TEXT NOT NULL,
        data_inicio TEXT,
        data_fim TEXT,
        mes_referencia TEXT,
        ano_referencia INTEGER,
        valor_total REAL,
        arquivo_pdf TEXT NOT NULL,
        arquivo_hash TEXT,
        data_upload TEXT NOT NULL,
        observacoes TEXT,
        FOREIGN KEY (id_conta) REFERENCES Contas(id_conta) ON DELETE CASCADE
    )
    ''')
    
    conn.commit()
    conn.close()

def carregar_contas_padrao():
    """Carrega todas as contas organizadas por fundo"""
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM Contas')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    contas = {
        'PMIP': {
            'BANPARA': ['8.304-6', '17.050-0', '17.105-0', '17.127-1', '36.767-2', '36.788-5', '36.789-3', '37.571-3', '37.572-1', '010.403-5', '128.506-8', '170.010-3', '170.011-1', '170.015-4', '170.022-7', '170.023-5', '170.025-1', '170.028-6', '170.030-8', '170.031-6', '170.032-4', '170.036-7', '170.040-5', '170.041-3', '170.043-0', '170.276-9', '375.695-5', '398.956-9', '400.023-4', '400.026-9', '400.027-7', '407.664-8', '407.670-2', '407.674-5', '407.675-3', '407.682-6', '428.788-6', '554.632-0', '601.376-7', '601.382-1', '602.404-1', '615.101-9', '639.742-5', '639.745-0', '754.822-2', '779.815-6', '794.524-8', '814.145-2', '829.230-2', '842.454-3', '846.313-1', '847.393-5', '847.410-9', '860.496-7', '894.576-4', '900.504-8', '916.972-5', '916.977-6', '916.983-0', '933.773-3', '948.869-3', '965.597-2', '966.976-0', '967.553-1'],
            'BB': ['110-4', '5.076-8', '6.770-9', '6.802-0', '7.040-8', '7.042-4', '7.043-2', '7.044-0', '7.045-9', '7.079-3', '7.219-2', '7.406-3', '7.545-0', '8.211-2', '8.242-2', '8.286-4', '8.309-7', '8.531-6', '8.597-9', '8.651-7', '8.697-5', '9.429-3', '9.457-9', '9.458-7', '9.459-5', '9.592-3', '9.718-7', '9.911-2', '10.262-8', '10.636-4', '10.892-8', '10.984-3', '11.007-8', '11.008-6', '11.009-4', '11.010-8', '11.012-4', '11.164-3', '11.224-0', '11.321-2', '11.400-6', '11.456-1', '11.466-9', '11.467-7', '11.486-3', '11.528-2', '11.629-7', '11.800-1', '11.829-X', '12.104-5', '12.105-3', '12.156-8', '12.552-0', '12.607-1', '13.523-2', '13.565-8', '13.717-0', '13.954-8', '14.223-9', '14.378-2', '14.435-5', '14.765-6', '14.766-4', '14.955-1', '15.085-1', '15.116-5', '15.139-4', '15.140-8', '15.214-5', '15.302-8', '15.303-6', '15.304-4', '15.305-2', '15.306-0', '15.326-5', '15.390-7', '15.623-X', '15.677-9', '15.700-7', '15.701-5', '15.702-3', '15.703-1', '16.089-X', '16.512-3', '16.514-X', '16.560-3', '17.096-8', '17.252-9', '19.963-X', '19.964-8', '19.965-6', '19.966-4', '21.715-8', '21.716-6', '21.717-4', '21.718-2', '21.719-0', '21.720-4', '22.741-2', '60.485-2', '60.636-7', '67.693-4', '68.814-2', '80.102-X', '283.143-0', '450.077-6', '450.092-X', '450.166-7', '450.233-7'],
            'BRADESCO': ['200-3', '310.200-9'],
            'CEF': ['1-7', '5-0', '6-8', '71.011-1', '71.014-6', '624.000-1', '624.001-0', '624.005-2', '624.006-0', '624.007-9', '624.008-7', '624.010-9', '624.011-7', '624.012-5', '624.014-1', '624.015-0', '624.016-8', '624.017-6', '624.018-4', '624.019-2', '624.020-6', '624.021-4', '624.022-2', '624.023-0', '624.024-9', '624.025-7', '647.002-8', '647.003-1', '647.005-8', '647.007-4', '647.010-4', '647.011-2', '647.012-0', '647.013-9', '647.014-7', '647.015-5', '574.172.156-3', '574.172.157-1', '574.172.158-0', '574.172.161-0', '574.172.162-8', '574.172.163-6', '574.172.164-4', '574.172.165-2', '574.172.166-0', '575.222.452-3', '575.222.453-1', '575.222.454-0', '575.222.455-8', '575.222.456-6', '575.829.746-8', '575.986.903-1', '575.986.904-0', '575.986.905-8', '575.986.906-6', '575.986.907-4', '575.986.908-2', '575.986.909-0', '575.986.911-2', '575.986.912-0', '575.986.913-9', '575.986.914-7', '575.986.915-5', '575.986.917-1', '575.986.918-0', '575.986.919-8', '575.986.921-0', '575.986.922-8', '575.986.923-6', '575.986.924-4', '575.986.925-2'],
            'SICREDI': ['04.977-4']
        },
        'CM': {
            'BANPARA': ['404.419-3'],
            'BB': ['12.076-6'],
            'SICREDI': ['05.274-7']
        },
        'FMS': {
            'BANPARA': ['017.113-1', '170.042-1', '400.021-8', '400.029-3', '779.815-6'],
            'BB': ['7.040-8', '7.042-4', '7.043-2', '7.044-0', '7.045-9', '7.079-3', '8.309-7', '9.718-7', '12.552-0', '15.302-8', '15.303-6', '15.304-4', '15.305-2', '19.963-X', '19.964-8', '19.965-6', '19.966-4', '21.715-8', '21.716-6', '21.717-4', '21.718-2', '21.719-0', '21.720-4', '22.741-2', '450.077-6'],
            'BRADESCO': ['2.000-1', '312.000-7'],
            'CEF': ['6-8', '624.000-1', '624.001-0', '624.002-8', '624.003-6', '624.004-4', '624.005-2', '624.006-0', '624.007-9', '624.008-7', '624.010-9', '624.011-7', '624.012-5', '624.013-3', '624.014-1', '624.015-0', '624.016-8', '624.017-6', '624.018-4', '624.019-2', '624.020-6', '624.021-4', '624.022-2', '624.023-0', '624.024-9', '624.025-7', '574.363.185-5', '574.686.559-8', '574.686.561-0', '574.686.562-8', '575.222.454-0', '575.829.746-8', '575.986.903-1', '575.986.904-0', '575.986.905-8', '575.986.906-6', '575.986.907-4', '575.986.908-2', '575.986.909-0', '575.986.911-2', '575.986.912-0', '575.986.913-9', '575.986.914-7', '575.986.915-5', '575.986.916-3', '575.986.917-1', '575.986.918-0', '575.986.919-8', '575.986.921-0', '575.986.922-8', '575.986.923-6', '575.986.924-4', '575.986.925-2'],
            'SICREDI': ['14.719-5']
        },
        'FME': {
            'BANPARA': ['17.066-6', '20.229-0', '170.024-3', '170.026-0', '170.044-8', '400.025-0', '601.376-7', '601.382-1', '615.099-3', '779.815-6', '846.313-1', '966.976-0', '967.553-1'],
            'BB': ['110-4', '7.219-2', '7.406-3', '7.545-0', '8.211-2', '8.242-2', '8.286-4', '8.531-6', '8.597-9', '8.697-5', '9.457-9', '9.592-3', '9.911-2', '10.262-8', '10.636-4', '10.984-3', '11.224-0', '11.528-2', '12.552-0', '12.607-1', '15.306-0', '15.326-5', '16.514-X', '60.485-2', '60.636-7', '67.693-4', '68.814-2', '80.102-X'],
            'CEF': ['6-8', '575.222.454-0']
        },
        'FMAS': {
            'BANPARA': ['779.815-6'],
            'BB': ['9.458-7', '9.459-5', '11.007-8', '11.008-6', '11.009-4', '11.010-8', '11.012-4', '11.400-6', '11.456-1', '11.486-3', '12.104-5', '12.105-3', '12.156-8', '12.552-0', '13.717-0', '13.954-8', '14.378-2', '14.435-5', '14.955-1', '15.623-X', '16.560-3', '17.096-8', '450.077-6'],
            'CEF': ['5-0', '6-8', '71.011-1', '575.222.453-1', '575.222.454-0', '575.222.455-8'],
            'SICREDI': ['04.977-4']
        },
        'FMMA': {
            'BANPARA': ['17.050-0', '779.815-6'],
            'BB': ['6.802-0', '15.116-5', '450.233-7'],
            'CEF': ['6-8', '575.222.454-0'],
            'SICREDI': ['04.977-4']
        },
        'FUNDEB': {
            'BANPARA': ['779.815-6'],
            'BB': ['12.607-1', '15.677-9', '16.512-3'],
            'CEF': ['6-8', '575.222.454-0']
        },
        'FMDCA': {
            'BB': ['11.829-X']
        }
    }
    
    for fundo, bancos in contas.items():
        for banco, numeros_conta in bancos.items():
            for numero_conta in numeros_conta:
                try:
                    cursor.execute('''
                    INSERT OR IGNORE INTO Contas (fundo, banco, numero_conta, agencia, tem_poupanca, tem_aplicacao, ativa)
                    VALUES (?, ?, ?, '4876', 0, 0, 1)
                    ''', (fundo, banco, numero_conta))
                except:
                    pass
    
    conn.commit()
    conn.close()
    print("[INFO] Contas carregadas por fundo!")

def detectar_tipos_documento(texto_completo):
    """
    Detecta TODOS os tipos de documentos presentes no PDF
    Retorna uma lista de tipos encontrados
    """
    tipos_encontrados = []
    texto_lower = texto_completo.lower()
    
    # Verificar Conciliação Bancária
    if 'conciliação bancária' in texto_lower or 'conciliacao bancaria' in texto_lower:
        tipos_encontrados.append('Conciliação Bancária')
    
    # Verificar Conta Corrente
    if 'extrato de conta corrente' in texto_lower or 'conta corrente' in texto_lower:
        tipos_encontrados.append('Conta Corrente')
    
    # Verificar Poupança
    if 'poupança' in texto_lower or 'poupanca' in texto_lower:
        tipos_encontrados.append('Conta Poupança')
    
    # Verificar Aplicação
    if any(palavra in texto_lower for palavra in ['aplicação', 'aplicacao', 'investimento', 'fundo', 'bb rf', 'consultas - investimentos']):
        tipos_encontrados.append('Conta de Aplicação')
    
    # Se não encontrou nada, assume Conta Corrente como padrão
    if not tipos_encontrados:
        tipos_encontrados.append('Conta Corrente')
    
    return tipos_encontrados

def extrair_informacoes_pdf(pdf_path):
    """
    Extrai AUTOMATICAMENTE todas as informações do PDF com LOGS DETALHADOS
    """
    print(f"\n{'='*80}")
    print(f"[INÍCIO] Processando PDF: {os.path.basename(pdf_path)}")
    print(f"{'='*80}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            texto_completo = ""
            print(f"[INFO] PDF tem {len(pdf.pages)} página(s)")
            
            for i, page in enumerate(pdf.pages, 1):
                texto = page.extract_text()
                if texto:
                    texto_completo += texto + "\n"
                    print(f"[INFO] Página {i}: {len(texto)} caracteres extraídos")
            
            if not texto_completo.strip():
                print(f"[ERRO] PDF está vazio ou não contém texto extraível")
                return None
            
            # Detectar tipos de documento
            print(f"\n[EXTRAÇÃO] Detectando tipos de documento...")
            tipos_documento = detectar_tipos_documento(texto_completo)
            print(f"[RESULTADO] Tipos encontrados: {', '.join(tipos_documento)}")
            
            numero_conta = extrair_numero_conta_multiplos_metodos(texto_completo)
            
            # Extrair agência
            print(f"\n[EXTRAÇÃO] Buscando agência...")
            agencia = None
            padroes_agencia = [
                r'AGENCIA[:\s]+(\d+[\-\.]?\d*)',
                r'Ag[eê]ncia[:\s]*(\d+[\-\.]?\d*)',
            ]
            
            for padrao in padroes_agencia:
                match = re.search(padrao, texto_completo, re.IGNORECASE)
                if match:
                    agencia = match.group(1).strip()
                    agencia = re.sub(r'[^\d]', '', agencia)
                    print(f"[OK] Agência encontrada: {agencia}")
                    break
            
            if not agencia:
                agencia = '4876'  # Padrão
                print(f"[PADRÃO] Usando agência padrão: 4876")
            
            # Extrair período
            print(f"\n[EXTRAÇÃO] Buscando período (datas)...")
            data_inicio = None
            data_fim = None
            
            # Método 1: Padrão "de DD/MM/YYYY até DD/MM/YYYY"
            match_periodo = re.search(r'de?\s*(\d{2}[\/\-]\d{2}[\/\-]\d{4})\s*até\s*(\d{2}[\/\-]\d{2}[\/\-]\d{4})', texto_completo, re.IGNORECASE)
            if match_periodo:
                data_inicio = match_periodo.group(1).replace('-', '/')
                data_fim = match_periodo.group(2).replace('-', '/')
                print(f"[OK] Período encontrado (método 1): {data_inicio} até {data_fim}")
            
            # Método 2: Buscar "Período do extrato"
            if not data_inicio:
                match_periodo2 = re.search(r'Per[ií]odo\s+do\s+extrato[:\s]*(\d{2}[\/\-]\d{2}[\/\-]\d{4})\s*até\s*(\d{2}[\/\-]\d{2}[\/\-]\d{4})', texto_completo, re.IGNORECASE)
                if match_periodo2:
                    data_inicio = match_periodo2.group(1).replace('-', '/')
                    data_fim = match_periodo2.group(2).replace('-', '/')
                    print(f"[OK] Período encontrado (método 2): {data_inicio} até {data_fim}")
            
            # Método 3: Buscar todas as datas e pegar primeira e última
            if not data_inicio:
                todas_datas = re.findall(r'\d{2}[\/\-]\d{2}[\/\-]\d{4}', texto_completo)
                if len(todas_datas) >= 2:
                    data_inicio = todas_datas[0].replace('-', '/')
                    data_fim = todas_datas[-1].replace('-', '/')
                    print(f"[OK] Período encontrado (método 3): {data_inicio} até {data_fim}")
            
            # Extrair mês e ano de referência
            print(f"\n[EXTRAÇÃO] Determinando mês/ano de referência...")
            mes_referencia = None
            ano_referencia = None
            
            # Método 1: Buscar "EM DD/MM/YYYY"
            match_data_ref = re.search(r'EM\s+(\d{2})/(\d{2})/(\d{4})', texto_completo, re.IGNORECASE)
            if match_data_ref:
                mes_referencia = match_data_ref.group(2)
                ano_referencia = int(match_data_ref.group(3))
                print(f"[OK] Referência (método 1): {mes_referencia}/{ano_referencia}")
            
            # Método 2: Extrair do período
            elif data_inicio and '/' in data_inicio:
                partes = data_inicio.split('/')
                mes_referencia = partes[1]
                ano_referencia = int(partes[2])
                print(f"[OK] Referência (método 2): {mes_referencia}/{ano_referencia}")
            
            # Método 3: Extrair do nome do arquivo se tiver padrão MM-YYYY
            if not mes_referencia:
                nome_arquivo = os.path.basename(pdf_path)
                match_nome = re.search(r'(\d{2})[-_](\d{4})', nome_arquivo)
                if match_nome:
                    mes_referencia = match_nome.group(1)
                    ano_referencia = int(match_nome.group(2))
                    print(f"[OK] Referência (método 3 - nome arquivo): {mes_referencia}/{ano_referencia}")
            
            periodo_completo = False
            if data_inicio and data_fim and mes_referencia and ano_referencia:
                periodo_completo = verificar_periodo_completo(data_inicio, data_fim, mes_referencia, ano_referencia)
            
            # Extrair valor total
            print(f"\n[EXTRAÇÃO] Buscando valor total...")
            valor_total = 0.0
            valores_encontrados = []
            
            for linha in texto_completo.split('\n'):
                if any(palavra in linha.lower() for palavra in ['saldo', 'total', 'saldo real']):
                    matches = re.findall(r'(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)', linha)
                    for match in matches:
                        try:
                            valor_str = match.replace('.', '').replace(',', '.')
                            valor = float(valor_str)
                            if 0.01 < valor < 100000000:
                                valores_encontrados.append(valor)
                        except:
                            pass
            
            if valores_encontrados:
                valor_total = max(valores_encontrados)
                print(f"[OK] Valor total: R$ {valor_total:.2f}")
            else:
                print(f"[AVISO] Valor total NÃO encontrado")
            
            # Valores padrão se necessário
            if not data_inicio:
                data_inicio = datetime.now().strftime('%d/%m/%Y')
                print(f"[PADRÃO] Data início: {data_inicio}")
            if not data_fim:
                data_fim = datetime.now().strftime('%d/%m/%Y')
                print(f"[PADRÃO] Data fim: {data_fim}")
            if not mes_referencia:
                mes_referencia = datetime.now().strftime('%m')
                print(f"[PADRÃO] Mês referência: {mes_referencia}")
            if not ano_referencia:
                ano_referencia = datetime.now().year
                print(f"[PADRÃO] Ano referência: {ano_referencia}")
            
            print(f"\n{'='*80}")
            print(f"[FIM] Processamento concluído")
            print(f"[RESUMO] Conta: {numero_conta} | Período: {data_inicio} a {data_fim} | Completo: {periodo_completo}")
            print(f"{'='*80}\n")
            
            return {
                'tipos_documento': tipos_documento,
                'numero_conta': numero_conta,
                'agencia': agencia,
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'mes_referencia': mes_referencia,
                'ano_referencia': ano_referencia,
                'valor_total': valor_total,
                'periodo_completo': periodo_completo
            }
            
    except Exception as e:
        print(f"\n[ERRO CRÍTICO] Erro ao extrair dados do PDF: {e}")
        import traceback
        traceback.print_exc()
        return None

def normalizar_numero_conta(numero_conta):
    """
    Normaliza número de conta para matching inteligente
    Remove zeros à esquerda, pontos, traços, espaços
    Preserva X no final
    """
    if not numero_conta:
        return None
    
    # Converter para string e uppercase
    numero = str(numero_conta).upper().strip()
    
    numero = numero.replace('.', '').replace('-', '').replace(' ', '')
    
    if numero.endswith('X'):
        parte_numerica = numero[:-1].lstrip('0')
        numero = parte_numerica + 'X' if parte_numerica else 'X'
    else:
        numero = numero.lstrip('0')
    
    print(f"[NORMALIZAÇÃO] '{numero_conta}' -> '{numero}'")
    return numero

def extrair_numero_conta_multiplos_metodos(texto_completo):
    """
    Extrai número da conta usando MÚLTIPLOS métodos
    para lidar com padrões aleatórios
    """
    print(f"\n[EXTRAÇÃO AVANÇADA] Buscando número da conta com múltiplos métodos...")
    
    candidatos = []
    
    # MÉTODO 1: CONTA: seguido de número
    metodo1 = re.findall(r'CONTA[:\s]+(\d+[\.\-]?\d*[\-]?\d*)', texto_completo, re.IGNORECASE)
    if metodo1:
        candidatos.extend(metodo1)
        print(f"[MÉTODO 1] Encontrados: {metodo1}")
    
    # MÉTODO 2: Conta corrente seguido de número
    metodo2 = re.findall(r'Conta\s+corrente[:\s]*(\d+[\.\-]?\d*[\-]?\d*)', texto_completo, re.IGNORECASE)
    if metodo2:
        candidatos.extend(metodo2)
        print(f"[MÉTODO 2] Encontrados: {metodo2}")
    
    # MÉTODO 3: Padrão com pontos e traço (ex: 8.304-6)
    metodo3 = re.findall(r'\b(\d{1,3}\.?\d{3}[\-]\d{1})\b', texto_completo)
    if metodo3:
        candidatos.extend(metodo3)
        print(f"[MÉTODO 3] Encontrados: {metodo3}")
    
    # MÉTODO 4: Padrão sem formatação (ex: 0000083046)
    metodo4 = re.findall(r'(?:Conta|CONTA)[:\s]*(\d{8,12})', texto_completo, re.IGNORECASE)
    if metodo4:
        candidatos.extend(metodo4)
        print(f"[MÉTODO 4] Encontrados: {metodo4}")
    
    # MÉTODO 5: Contas com X no final (ex: 15623-X)
    metodo5 = re.findall(r'\b(\d{1,3}\.?\d{3}[\-][Xx])\b', texto_completo)
    if metodo5:
        candidatos.extend(metodo5)
        print(f"[MÉTODO 5] Encontrados: {metodo5}")
    
    # MÉTODO 6: Buscar após "Conta corrente" ou "CONTA:" em linhas específicas
    linhas = texto_completo.split('\n')
    for i, linha in enumerate(linhas):
        if 'conta corrente' in linha.lower() or 'conta:' in linha.lower():
            # Procurar número na mesma linha ou nas próximas 2 linhas
            texto_busca = ' '.join(linhas[i:min(i+3, len(linhas))])
            numeros = re.findall(r'\b(\d{4,12}[\-]?\d?)\b', texto_busca)
            if numeros:
                candidatos.extend(numeros)
                print(f"[MÉTODO 6] Encontrados na linha {i}: {numeros}")
    
    # Remover duplicatas e normalizar
    candidatos_unicos = list(set(candidatos))
    
    if not candidatos_unicos:
        print(f"[FALHA] Nenhum candidato encontrado por nenhum método")
        return None
    
    print(f"[RESULTADO] {len(candidatos_unicos)} candidato(s) encontrado(s): {candidatos_unicos}")
    
    # Retornar o primeiro candidato mais provável
    # Priorizar números com formatação (pontos e traços)
    for candidato in candidatos_unicos:
        if '.' in candidato or '-' in candidato:
            print(f"[SELECIONADO] Conta com formatação: {candidato}")
            return candidato
    
    # Se não houver com formatação, retornar o primeiro
    print(f"[SELECIONADO] Primeiro candidato: {candidatos_unicos[0]}")
    return candidatos_unicos[0]

def buscar_conta_por_numero(numero_conta):
    """
    Busca conta usando normalização inteligente
    """
    if not numero_conta:
        return None
    
    numero_normalizado = normalizar_numero_conta(numero_conta)
    
    if not numero_normalizado:
        return None
    
    print(f"[BUSCA] Procurando conta normalizada: '{numero_normalizado}'")
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id_conta, numero_conta, fundo, banco FROM Contas WHERE ativa = 1
    ''')
    
    todas_contas = cursor.fetchall()
    
    for conta in todas_contas:
        conta_normalizada = normalizar_numero_conta(conta['numero_conta'])
        if conta_normalizada == numero_normalizado:
            print(f"[MATCH!] Encontrada: Fundo={conta['fundo']}, Banco={conta['banco']}, Conta={conta['numero_conta']}")
            conn.close()
            return conta['id_conta']
    
    print(f"[SEM MATCH] Conta '{numero_normalizado}' não encontrada no banco")
    conn.close()
    return None

def verificar_periodo_completo(data_inicio, data_fim, mes_ref, ano_ref):
    """
    Verifica se o período do extrato cobre o mês COMPLETO
    MUITO IMPORTANTE: retorna True se cobre o mês inteiro, False caso contrário
    """
    try:
        from datetime import datetime
        import calendar
        
        # Converter datas para objetos datetime
        dia_inicio = int(data_inicio.split('/')[0])
        mes_inicio = int(data_inicio.split('/')[1])
        ano_inicio = int(data_inicio.split('/')[2])

        dia_fim = int(data_fim.split('/')[0])
        mes_fim = int(data_fim.split('/')[1])
        ano_fim = int(data_fim.split('/')[2])

        mes_ref_int = int(mes_ref)
        ano_ref_int = int(ano_ref)

        # Garantir que o período está no mesmo ano de referência
        if ano_inicio != ano_ref_int or ano_fim != ano_ref_int:
            print(f"[AVISO] Período NÃO está no ano {ano_ref_int}")
            return False

        # Verificar se é o mesmo mês
        if mes_inicio != mes_ref_int or mes_fim != mes_ref_int:
            print(f"[AVISO] Período NÃO está no mês {mes_ref_int}/{ano_ref_int}")
            return False
        
        # Verificar se começa no dia 1
        if dia_inicio != 1:
            print(f"[AVISO] Período NÃO começa no dia 1 (começa no dia {dia_inicio})")
            return False
        
        # Verificar se termina no último dia do mês
        ultimo_dia = calendar.monthrange(ano_ref, mes_ref_int)[1]
        if dia_fim != ultimo_dia:
            print(f"[AVISO] Período NÃO termina no último dia do mês {ultimo_dia} (termina no dia {dia_fim})")
            return False
        
        print(f"[OK] Período COMPLETO: {data_inicio} a {data_fim}")
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro ao verificar período: {e}")
        return False

def calcular_hash_arquivo(caminho_arquivo):
    """Calcula hash MD5 do arquivo para detectar duplicatas"""
    hash_md5 = hashlib.md5()
    with open(caminho_arquivo, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

@app.route('/')
def index():
    conn = conectar_db()
    cursor = conn.cursor()
    
    filtro_fundo = request.args.get('fundo', 'TODAS')
    filtro_mes = request.args.get('mes', '')
    filtro_ano = request.args.get('ano', '')
    
    query = '''
    SELECT 
        c.*,
        GROUP_CONCAT(DISTINCT CASE WHEN d.tipo_documento = 'Conciliação Bancária' THEN d.id_documento || ':' || d.arquivo_pdf || ':' || d.mes_referencia || '/' || d.ano_referencia END) as docs_conciliacao,
        GROUP_CONCAT(DISTINCT CASE WHEN d.tipo_documento = 'Conta Corrente' THEN d.id_documento || ':' || d.arquivo_pdf || ':' || d.mes_referencia || '/' || d.ano_referencia END) as docs_corrente,
        GROUP_CONCAT(DISTINCT CASE WHEN d.tipo_documento = 'Conta Poupança' THEN d.id_documento || ':' || d.arquivo_pdf || ':' || d.mes_referencia || '/' || d.ano_referencia END) as docs_poupanca,
        GROUP_CONCAT(DISTINCT CASE WHEN d.tipo_documento = 'Conta de Aplicação' THEN d.id_documento || ':' || d.arquivo_pdf || ':' || d.mes_referencia || '/' || d.ano_referencia END) as docs_aplicacao,
        MIN(d.data_inicio) as periodo_inicio,
        MAX(d.data_fim) as periodo_fim,
        d.mes_referencia,
        d.ano_referencia
    FROM Contas c
    LEFT JOIN Documentos d ON c.id_conta = d.id_conta
    WHERE c.ativa = 1
    '''
    
    params = []
    
    if filtro_fundo != 'TODAS':
        query += ' AND c.fundo = ?'
        params.append(filtro_fundo)
    
    if filtro_mes:
        query += ' AND d.mes_referencia = ?'
        params.append(filtro_mes)
    
    if filtro_ano:
        query += ' AND d.ano_referencia = ?'
        params.append(int(filtro_ano))
    
    query += ' GROUP BY c.id_conta ORDER BY c.fundo, c.banco, c.numero_conta'
    
    cursor.execute(query, params)
    todas_contas = cursor.fetchall()
    
    cursor.execute('SELECT DISTINCT fundo FROM Contas ORDER BY fundo')
    fundos_disponiveis = [row['fundo'] for row in cursor.fetchall()]
    
    cursor.execute('''
    SELECT DISTINCT mes_referencia, ano_referencia 
    FROM Documentos 
    WHERE mes_referencia IS NOT NULL AND ano_referencia IS NOT NULL
    ORDER BY ano_referencia DESC, mes_referencia DESC
    ''')
    periodos_disponiveis = cursor.fetchall()
    
    conn.close()
    
    contas_organizadas = {}
    for conta in todas_contas:
        fundo = conta['fundo']
        banco = conta['banco']
        
        if fundo not in contas_organizadas:
            contas_organizadas[fundo] = {}
        
        if banco not in contas_organizadas[fundo]:
            contas_organizadas[fundo][banco] = []
        
        contas_organizadas[fundo][banco].append(conta)
    
    return render_template('index.html', 
                         contas_organizadas=contas_organizadas,
                         fundos_disponiveis=fundos_disponiveis,
                         periodos_disponiveis=periodos_disponiveis,
                         filtro_fundo=filtro_fundo,
                         filtro_mes=filtro_mes,
                         filtro_ano=filtro_ano)

@app.route('/upload-multiplo', methods=['POST'])
def upload_multiplo():
    """
    Upload de MÚLTIPLOS arquivos PDF com detecção automática e prevenção de duplicatas
    """
    print(f"\n{'#'*80}")
    print(f"# INICIANDO UPLOAD MÚLTIPLO")
    print(f"{'#'*80}\n")
    
    if 'documentos' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
    
    arquivos = request.files.getlist('documentos')
    print(f"[INFO] {len(arquivos)} arquivo(s) recebido(s)")
    
    resultados = []
    erros = []
    duplicatas = []
    
    for idx, arquivo in enumerate(arquivos, 1):
        print(f"\n{'='*80}")
        print(f"[{idx}/{len(arquivos)}] Processando: {arquivo.filename}")
        print(f"{'='*80}")
        
        if arquivo.filename == '' or not allowed_file(arquivo.filename):
            msg = f"{arquivo.filename}: arquivo inválido"
            print(f"[ERRO] {msg}")
            erros.append(msg)
            continue
        
        try:
            nome_original = secure_filename(arquivo.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            nome_arquivo = f"{timestamp}_{nome_original}"
            caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
            arquivo.save(caminho_arquivo)
            print(f"[OK] Arquivo salvo temporariamente")
            
            # Calcular hash para detectar duplicatas
            hash_arquivo = calcular_hash_arquivo(caminho_arquivo)
            print(f"[INFO] Hash do arquivo: {hash_arquivo}")
            
            # Verificar se já existe
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute('SELECT arquivo_pdf FROM Documentos WHERE arquivo_hash = ?', (hash_arquivo,))
            arquivo_existente = cursor.fetchone()
            
            if arquivo_existente:
                os.remove(caminho_arquivo)
                msg = f"{nome_original}: DUPLICATA detectada (já existe como {arquivo_existente['arquivo_pdf']})"
                print(f"[AVISO] {msg}")
                duplicatas.append(msg)
                conn.close()
                continue
            
            # Extrair informações
            info = extrair_informacoes_pdf(caminho_arquivo)
            
            if not info:
                os.remove(caminho_arquivo)
                msg = f"{nome_original}: erro ao ler PDF"
                print(f"[ERRO] {msg}")
                erros.append(msg)
                conn.close()
                continue
            
            id_conta = None
            if info['numero_conta']:
                id_conta = buscar_conta_por_numero(info['numero_conta'])
            
            if not id_conta:
                os.remove(caminho_arquivo)
                msg_erro = f"{nome_original}: Conta não encontrada"
                if info['numero_conta']:
                    msg_erro += f" (Conta: {info['numero_conta']})"
                print(f"[ERRO] {msg_erro}")
                erros.append(msg_erro)
                conn.close()
                continue
            
            # Salvar documentos
            documentos_salvos = []
            for tipo_doc in info['tipos_documento']:
                cursor.execute('''
                INSERT INTO Documentos (id_conta, tipo_documento, data_inicio, data_fim, 
                                       mes_referencia, ano_referencia, valor_total, 
                                       arquivo_pdf, arquivo_hash, data_upload, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (id_conta, tipo_doc, info['data_inicio'], info['data_fim'], 
                      info['mes_referencia'], info['ano_referencia'], info['valor_total'], 
                      nome_arquivo, hash_arquivo, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                      f"Upload automático - {nome_original}"))
                documentos_salvos.append(tipo_doc)
                print(f"[OK] Documento salvo: {tipo_doc}")
            
            conn.commit()
            conn.close()
            
            resultados.append({
                'arquivo': nome_original,
                'conta': info['numero_conta'],
                'tipos': documentos_salvos
            })
            
            print(f"[SUCESSO] {nome_original} processado com êxito!")
            
        except Exception as e:
            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)
            msg = f"{nome_original}: {str(e)}"
            print(f"[ERRO] {msg}")
            erros.append(msg)
    
    print(f"\n{'#'*80}")
    print(f"# UPLOAD MÚLTIPLO FINALIZADO")
    print(f"# Sucesso: {len(resultados)} | Erros: {len(erros)} | Duplicatas: {len(duplicatas)}")
    print(f"{'#'*80}\n")
    
    return jsonify({
        'sucesso': len(resultados),
        'erros': len(erros),
        'duplicatas': len(duplicatas),
        'resultados': resultados,
        'mensagens_erro': erros,
        'mensagens_duplicata': duplicatas
    })

@app.route('/ver-documentos/<int:id_conta>')
def ver_documentos(id_conta):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Contas WHERE id_conta = ?', (id_conta,))
    conta = cursor.fetchone()
    
    if not conta:
        flash('Conta não encontrada', 'error')
        return redirect(url_for('index'))
    
    cursor.execute('''
    SELECT * FROM Documentos
    WHERE id_conta = ?
    ORDER BY ano_referencia DESC, mes_referencia DESC, tipo_documento
    ''', (id_conta,))
    
    documentos = cursor.fetchall()
    conn.close()
    
    return render_template('ver_documentos.html', conta=conta, documentos=documentos)

@app.route('/editar-conta/<int:id_conta>', methods=['GET', 'POST'])
def editar_conta(id_conta):
    conn = conectar_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        tem_poupanca = 1 if request.form.get('tem_poupanca') else 0
        tem_aplicacao = 1 if request.form.get('tem_aplicacao') else 0
        
        cursor.execute('''
        UPDATE Contas 
        SET tem_poupanca = ?, tem_aplicacao = ?
        WHERE id_conta = ?
        ''', (tem_poupanca, tem_aplicacao, id_conta))
        
        conn.commit()
        conn.close()
        
        flash('Configurações da conta atualizadas!', 'success')
        return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM Contas WHERE id_conta = ?', (id_conta,))
    conta = cursor.fetchone()
    conn.close()
    
    return render_template('editar_conta.html', conta=conta)

@app.route('/deletar-documento/<int:id_documento>')
def deletar_documento(id_documento):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT arquivo_pdf, id_conta FROM Documentos WHERE id_documento = ?', (id_documento,))
    resultado = cursor.fetchone()
    
    if resultado:
        # Verificar se outros documentos usam o mesmo arquivo
        cursor.execute('SELECT COUNT(*) FROM Documentos WHERE arquivo_pdf = ?', (resultado['arquivo_pdf'],))
        count = cursor.fetchone()[0]
        
        # Se for o último documento usando este arquivo, deletar o arquivo
        if count == 1:
            caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], resultado['arquivo_pdf'])
            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)
        
        cursor.execute('DELETE FROM Documentos WHERE id_documento = ?', (id_documento,))
        conn.commit()
        
        id_conta = resultado['id_conta']
        conn.close()
        
        flash('Documento deletado com sucesso!', 'success')
        return redirect(url_for('ver_documentos', id_conta=id_conta))
    
    conn.close()
    flash('Documento não encontrado', 'error')
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/visualizar-pdf/<int:id_documento>')
def visualizar_pdf(id_documento):
    """Retorna o PDF para visualização inline"""
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT arquivo_pdf FROM Documentos WHERE id_documento = ?', (id_documento,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return send_from_directory(app.config['UPLOAD_FOLDER'], resultado['arquivo_pdf'])
    
    return "Arquivo não encontrado", 404

if __name__ == '__main__':
    inicializar_db()
    carregar_contas_padrao()
    app.run(debug=True, port=5000)
