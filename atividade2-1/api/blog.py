import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_ID = "1tlyG0wgHlhH2kWzgfjbaALouIHeg-N8-g5FKH-HQvRs"


def conectar_sheet():
    creds_dict = json.loads(os.environ["GOOGLE_CREDS"])

    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    return client.open_by_key(SHEET_ID).sheet1


def handler(request):
    try:
        sheet = conectar_sheet()

        if request.method == "GET":
            dados = sheet.get_all_values()

            mensagens = []
            for linha in dados:
                if len(linha) >= 2:
                    mensagens.append({
                        "author": linha[0],
                        "message": linha[1]
                    })

            return {
                "statusCode": 200,
                "body": json.dumps(mensagens[::-1]),
                "headers": {"Content-Type": "application/json"}
            }

        elif request.method == "POST":
            body = json.loads(request.body)

            action = body.get("action")
            message = body.get("message")
            author = body.get("author")

            if action != "put" or not message or not author:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Payload inválido"})
                }

            sheet.append_row([author, message])

            return {
                "statusCode": 200,
                "body": json.dumps({"status": "ok"})
            }

        else:
            return {
                "statusCode": 405,
                "body": json.dumps({"error": "Método não permitido"})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
