from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import subprocess

HOST = 'localhost'
PORT = 7070


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/home':
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
        <label for="src_ip">Введите IP-адрес источника:</label>
        <input type="text" id="src_ip" name="src_ip" value="10.1.1.7">
        
        <label for="dst_ip">Введите IP-адрес назначения:</label>
        <input type="text" id="dst_ip" name="dst_ip" value="10.1.1.8">
        
        <label for="password">Введите пароль:</label>
        <input type="password" id="password" name="password" value="547172" oninput="maskPassword()">
        
        <button onclick="window.location.href='/run_tuntap'">Запуск TAP интерфейса</button>
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
        src_ip = form.get('src_ip', [''])[0]
        dst_ip = form.get('dst_ip', [''])[0]
        password = form.get('password', [''])[0]
        current_dir = '/home/tot/FilePack'
        command = f"echo {password} | sudo -S gnome-terminal --geometry=200x24 -- bash -c './daemon_tap.py --current_dir {current_dir} --src_ip {src_ip} --dst_ip {dst_ip}'"
        subprocess.Popen(command, shell=True)

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        response = f'<p>TAP запущен успешно</p>'
        self.wfile.write(response.encode('utf-8'))


with HTTPServer((HOST, PORT), MyHandler) as server:
    print(f'Server running on http://{HOST}:{PORT}')
    server.serve_forever()