# 🗂️ Automação de Monitoramento de Backups

Este script automatiza a verificação e o envio de relatórios diários sobre os backups realizados em diferentes sistemas e servidores. O relatório é enviado por e-mail em formato de tabela HTML estilizada e também salvo como arquivo `.txt`.

## 📌 Objetivo

Garantir o controle diário da integridade dos backups realizados na unidade `E:\Backup`, verificando:

- Data mais antiga e mais recente de modificação em cada pasta.
- Status atualizado (✅ Em dia / ❌ Atrasado).
- Envio automático de e-mail com os dados.

---

## ⚙️ Como Funciona

- Percorre recursivamente as pastas de backup.
- Registra as datas de modificação mais antigas e mais recentes.
- Avalia o status do backup com base na data mais recente.
- Gera um relatório .txt com separadores ;.
- Gera uma tabela em HTML com cores indicativas.
- Envia o relatório por e-mail para o(s) destinatário(s).

## 📧 Estilo do E-mail

| **SISTEMA**    | **MAIS ANTIGO**     | **MAIS RECENTE**    | **STATUS**     |
| -------------- | ------------------- | ------------------- | -------------- |
| BANCO DE DADOS | 01/06/2025 01:00:00 | 04/06/2025 01:00:00 | ✅ **Em dia**   |
| SIGhRA         | 30/05/2025 22:00:00 | 03/06/2025 23:59:00 | ❌ **Atrasado** |
| SIRIUS         | 28/05/2025 04:00:00 | 04/06/2025 02:00:00 | ✅ **Em dia**   |
| UNIFI          | 01/06/2025 00:00:00 | 04/06/2025 01:30:00 | ✅ **Em dia**   |
| PABX SEMANAL   | 26/05/2025 20:00:00 | 27/05/2025 20:00:00 | ❌ **Atrasado** |
| PABX MENSAL    | 01/05/2025 02:00:00 | 01/06/2025          | ❌ **Atrasado** |

---

## ✏️ Configurações

```bash
PASTA_RAIZ = r"E:\Backup"
PASTA_RELATORIOS = r"E:\Scripts\relatorios_automacao_backups"

REMETENTE = "remetente.exemplo@gmail.com.br"
DESTINATARIO = "destinatario.exemplo@gmail.com.br"
COPIA = "emaildecopia.exemplo@gmail.com.br"
ASSUNTO = "Relatório de Backups Servidor"
```
📌 Importante: Insira a senha do e-mail do remetente na função enviar_email() para que o envio funcione corretamente.

## 🐍 Execução
Execute com Python 3:

```bash
python main.py
```

Ao final, será exibido:

```bash
🔍 Verificando backups...
✅ Verificação concluída.
✅ E-mail enviado com sucesso.
🟢 Pressione ENTER para sair...
```

## 📄 Exemplo de Relatório .txt
```bash
BANCO DE DADOS;12/05/2025 02:13:00;03/06/2025 02:14:01;Em dia
SIGhRA;10/05/2025 01:45:00;03/06/2025 03:00:00;Em dia
SIRIUS;08/05/2025 05:00:00;01/06/2025 02:50:00;Atrasado
...
```

## 🛠️ Dependências
- Python 3.x
- Módulos padrão: os, smtplib, datetime, email

## 🔒 Segurança
- Este script utiliza SMTP com starttls() para envio seguro de e-mail.
- Nunca publique ou compartilhe o script com a senha do e-mail preenchida.

## 🧠 Autor
Automação desenvolvida por mim para uso interno da equipe de TI da empresa J&C Gestão de Riscos.
