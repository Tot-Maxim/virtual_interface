from http.server import BaseHTTPRequestHandler, HTTPServer
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
<html lang="en">
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
     <form action="/run_tuntap">
        <label for="src_ip">Введите IP-адрес источника:</label>
        <input type="text" id="src_ip" name="src_ip" value="10.1.1.7">
        
        <label for="dst_ip">Введите IP-адрес назначения:</label>
        <input type="text" id="dst_ip" name="dst_ip" value="10.1.1.8">
        
        <label for="password">Введите пароль:</label>
        <input type="password" id="password" name="password" value="111111" oninput="maskPassword()">
        
       
        <button onclick="location.href='/home/run_tuntap'; return false;">Запуск TAP интерфейса</button>
    </form>
    <div id="output"></div>
</body>
</html>
"""
            self.wfile.write(html.encode('utf-8'))
        elif self.path == '/home/run_tuntap':
            try:
                src_ip = '10.1.1.7'
                dst_ip = '10.1.1.8'
                password = '111111'
                command = (f"echo {password} | sudo -S gnome-terminal --geometry=200x24 -- bash -c './daemon_tap.py "
                           f"--src_ip {src_ip} --dst_ip {dst_ip}'")
                rc = subprocess.Popen(command, shell=True)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Script execution initiated!')
            except subprocess.CalledProcessError as e:
                self.send_error(500, 'Error running script: ' + str(e))
        else:
            self.send_error(404, 'Not found')


with HTTPServer((HOST, PORT), MyHandler) as server:
    print(f'Server running on http://{HOST}:{PORT}')
    server.serve_forever()
