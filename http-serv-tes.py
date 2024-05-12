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
    <title>Simple Server</title>
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

        button {
            background-color: white;
            color: black;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <button onclick="window.location.href='/run_script'">Run.sh</button>
</body>
</html>
"""
            self.wfile.write(html.encode('utf-8'))
        elif self.path == '/run_script':
            try:
                subprocess.run(['./run.sh'], check=True)  # Execute run.sh
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