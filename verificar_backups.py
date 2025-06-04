import os
import smtplib  # Envio de e-mails via SMTP
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# configurações
PASTA_RAIZ = r"E:\Backup"
PASTA_RELATORIOS = r"E:\Scripts\relatorios_automacao_backups"

REMETENTE = "remetente.exemplo@gmail.com.br"
DESTINATARIO = "destinatario.exemplo@gmail.com.br"
COPIA = "emaildecopia.exemplo@gmail.com.br"
ASSUNTO = "Relatório de Backups Servidor"

# função para buscar as datas de modificação de arquivos em uma pasta
def buscar_datas_em(pasta):
    datas = []

    if not os.path.exists(pasta):
        return "Nenhuma", "Nenhuma", "Atrasado"

    for raiz, _, arquivos in os.walk(pasta):
        for arq in arquivos:
            try:
                caminho = os.path.join(raiz, arq)
                modificado = datetime.fromtimestamp(os.path.getmtime(caminho))
                datas.append(modificado)
            except:
                # ignora erros de leitura de arquivos específicos
                pass

    if not datas:
        return "Nenhuma", "Nenhuma", "Atrasado"

    mais_antigo = min(datas)
    mais_recente = max(datas)
    status = "Em dia" if mais_recente.date() == datetime.today().date() else "Atrasado"

    return (
        mais_antigo.strftime("%d/%m/%Y %H:%M:%S"),
        mais_recente.strftime("%d/%m/%Y %H:%M:%S"),
        status
    )

# função para montar os dados de todas as pastas
def gerar_dados():
    dados = []
    print("🔍 Verificando backups...")

    # pastas principais
    dados.append(["BANCO DE DADOS", *buscar_datas_em(os.path.join(PASTA_RAIZ, "BANCO DE DADOS"))])

    # SIGhRA (com OLD e Upload separados)
    antiga, _, _ = buscar_datas_em(os.path.join(PASTA_RAIZ, "SIGhRA", "OLD"))
    _, recente, status = buscar_datas_em(os.path.join(PASTA_RAIZ, "SIGhRA", "Upload"))
    dados.append(["SIGhRA", antiga, recente, status])

    # demais pastas diretas
    dados.append(["SIRIUS", *buscar_datas_em(os.path.join(PASTA_RAIZ, "SIRIUS"))])
    dados.append(["UNIFI", *buscar_datas_em(os.path.join(PASTA_RAIZ, "UNIFI"))])
    dados.append(["PABX SEMANAL", *buscar_datas_em(os.path.join(PASTA_RAIZ, "PABX", "Semanal"))])
    dados.append(["PABX MENSAL", *buscar_datas_em(os.path.join(PASTA_RAIZ, "PABX", "Mensal"))])

    # OMNILINK MR
    antiga, _, _ = buscar_datas_em(os.path.join(PASTA_RAIZ, "OMNILINK", "MR", "OLD"))
    _, recente, status = buscar_datas_em(os.path.join(PASTA_RAIZ, "OMNILINK", "MR", "Upload"))
    dados.append(["OMNILINK MR", antiga, recente, status])

    # OMNILINK SE
    antiga, _, _ = buscar_datas_em(os.path.join(PASTA_RAIZ, "OMNILINK", "SE", "OLD"))
    _, recente, status = buscar_datas_em(os.path.join(PASTA_RAIZ, "OMNILINK", "SE", "Upload"))
    dados.append(["OMNILINK SE", antiga, recente, status])

    # SERVIDORES
    servidores = [
        ("ANDROMEDA", os.path.join(PASTA_RAIZ, "SERVIDORES", "ANDROMEDA")),
        ("ARIES", os.path.join(PASTA_RAIZ, "SERVIDORES", "ARIES", "Container_Arquivos")),
        ("DRACO", os.path.join(PASTA_RAIZ, "SERVIDORES", "DRACO", "WindowsImageBackup", "DRACO")),
        ("PEIXES", os.path.join(PASTA_RAIZ, "SERVIDORES", "PEIXES", "WindowsImageBackup", "PEIXES")),
        ("SAGITARIUS", os.path.join(PASTA_RAIZ, "SERVIDORES", "SAGITARIUS", "01 - APLICAÇÕES")),
    ]

    for nome, caminho in servidores:
        _, recente, status = buscar_datas_em(caminho)
        dados.append([nome, "-", recente, status])

    print("✅ Verificação concluída.")
    return dados

# gera HTML estilizado para e-mail
def gerar_tabela_html(dados):
    html = """
    <html>
    <head>
    <style>
        body { font-family: Arial, sans-serif; font-size: 12px; text-align: center; }
        table { border-collapse: collapse; width: 90%; margin: auto; }
        th {
            background-color: #28a745;
            color: white;
            padding: 8px;
            border: 1px solid #ddd;
        }
        td {
            border: 1px solid #ddd;
            padding: 8px;
            background-color: #2e2e2e;
            color: white;
        }
        .em-dia { color: #28a745; font-weight: bold; }
        .atrasado { color: #dc3545; font-weight: bold; }
    </style>
    </head>
    <body>
        <h4>Arquivos Locais 'E:\\Backup' em Leao</h4>
        <table>
            <tr>
                <th>SISTEMA</th>
                <th>MAIS ANTIGO</th>
                <th>MAIS RECENTE</th>
                <th>STATUS</th>
            </tr>
    """

    for sistema, antiga, recente, status in dados:
        status_class = "em-dia" if status == "Em dia" else "atrasado"
        html += f"""
            <tr>
                <td>{sistema}</td>
                <td>{antiga}</td>
                <td>{recente}</td>
                <td class="{status_class}">{status}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """
    return html

# salva backup em .txt para histórico
def salvar_txt(dados):
    hoje = datetime.now().strftime('%d-%m-%Y')
    nome_arquivo = f"BACKUP-{hoje}.txt"
    caminho = os.path.join(PASTA_RELATORIOS, nome_arquivo)

    with open(caminho, 'w', encoding='utf-8') as f:
        for linha in dados:
            f.write(";".join(linha) + "\n")

# envia o e-mail com HTML formatado
def enviar_email(html):
    msg = MIMEMultipart('alternative')
    msg['From'] = REMETENTE
    msg['To'] = DESTINATARIO
    msg['Cc'] = COPIA
    msg['Subject'] = ASSUNTO

    msg.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as servidor:
            servidor.starttls()
            servidor.login(REMETENTE, "")  # insira a senha do email do remetente aqui (ou use variáveis de ambiente)
            servidor.send_message(msg)
        print("✅ E-mail enviado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao enviar o e-mail: {e}")

# execução principal
if __name__ == "__main__":
    dados = gerar_dados()
    salvar_txt(dados)
    html = gerar_tabela_html(dados)
    enviar_email(html)
    input("\n🟢 Pressione ENTER para sair...")
