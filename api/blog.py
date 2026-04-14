from http.server import BaseHTTPRequestHandler
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


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        sheet = conectar_sheet()
        dados = sheet.get_all_values()

        mensagens = []
        for linha in dados:
            if len(linha) >= 2:
                mensagens.append({
                    "author": linha[0],
                    "message": linha[1]
                })

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(mensagens[::-1]).encode())

    def do_POST(self):
        sheet = conectar_sheet()

        content_length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(content_length))

        action = body.get("action")
        message = body.get("message")
        author = body.get("author")

        if action != "put" or not message or not author:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Payload inválido"}).encode())
            return

        sheet.append_row([author, message])

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())
