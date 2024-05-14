from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import subprocess

HOST = 'localhost'
PORT = 7070


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/home/run_tuntap':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
<!DOCTYPE html>
<html lang='ru'>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TAP interface</title>
    <style>
        body {
            background-color: black;
            margin: 0;
            padding: 0;
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        form {
            display: grid;
            gap: 10px;
            justify-items: center;
            margin-top: 20px;
        }

        button {
            background-color: white;
            color: black;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }

        input {
            padding: 5px;
        }

        label {
            color: white;
            text-align: right;
            padding-right: 10px;
            grid-column: 1 / 2;
        }
    </style>
</head>
<body>
    <h1>Text Parser</h1>
    <form method="post">
        <label for="dst_ip">Введите IP-адрес сервера:</label>
        <input type="text" id="dst_ip" name="dst_ip" value="10.1.1.8">
        
        <label for="port">Введите порт сервера:</label>
        <input type="number" id="port" name="port" value=5050>
        
        <label for="file_path">Введите имя файла для передачи:</label>
        <input type="text" id="file_path" name="file_path" value='logo.png'>
        
        <button onclick="window.location.href='/run_tuntap'">Передать файл</button>
    </form>
    <div id="text_output"></div>
</body>
</html>
"""
            self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form = parse_qs(post_data)
        dst_ip = form.get('dst_ip', [''])[0]
        port = form.get('port', [''])[0]
        file_path = form.get('file_path', [''])[0]
        command = f"./interface.py"
        subprocess.Popen(command, shell=True)

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        response = f'<p>файл отправлен успешно</p>'
        self.wfile.write(response.encode('utf-8'))


with HTTPServer((HOST, PORT), MyHandler) as server:
    print(f'Server running on http://{HOST}:{PORT}')
    server.serve_forever()