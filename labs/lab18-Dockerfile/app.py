import http.server
import socketserver
import os

PORT = 8080
NOME_APP = os.getenv("APP_NAME", "Servico-Padrao")

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        mensagem = f"<h1>Sistema: {NOME_APP} | Status: Operacional</h1>"
        self.wfile.write(mensagem.encode("utf-8"))

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Aplicação [{NOME_APP}] ativa na porta {PORT}...")
    httpd.serve_forever()
