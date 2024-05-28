html_TAP = """
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

        <label for="file_path">Введите путь к папке обмена:</label>
        <input type="text" id="file_path" name="file_path" value='/home/tot/FilePack'>

        <button onclick="window.location.href='/home/serv/run_tuntap'">Запуск TAP интерфейса</button>
    </form>
    <div id="text_output"></div>
</body>
</html>
"""

socket_client = """
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
        <input type="text" id="client_ip" name="client_ip" value="10.1.1.8">

        <label for="port">Введите порт сервера:</label>
        <input type="number" id="client_port" name="client_port" value=5050>

        <label for="file_path">Введите имя файла для передачи:</label>
        <input type="text" id="file_path" name="file_path" value='logo.png'>

         <button onclick="redirect_client()">Передать файл</button>
    </form>
    <div id="text_output"></div>
    <script>
        function redirect_client() {
            window.location.href = '/choose';
        }
    </script>
    
</body>
</html>
"""

choose = '''
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
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }

        .button-container {
            display: flex;
            justify-content: space-between;
            width: 25%;
            margin-top: 20px; /* Отступ сверху */
            margin-bottom: 20px; /* Отступ снизу */
            margin-left: 20px; /* Отступ слева */
            margin-right: 20px; /* Отступ справа */
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


    </style>
</head>
<body>
<div class="button-container">
    <button onclick="redirect_server()">Запуск сервера</button>
    <button onclick="redirect_client()">Запуск клиента</button>
</div>
    <script>
        function redirect_server() {
            window.location.href = '/home/server';
        }
        function redirect_client() {
            window.location.href = '/home/client';
        }
    </script>
</body>
</html>
'''

socket_server = '''
<!DOCTYPE html>
<html lang='ru'>
<head>
<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server receive</title>
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
    <div>
    <h1>Server receive</h1>
    <form>
        <label for="dst_ip">Введите IP-адрес сервера:</label>
        <input type="text" id="socket_ip" name="socket_ip" value="10.1.1.8">
        
        <label for="dst_ip">Введите порт сервера:</label>
        <input type="number" id="socket_port" name="socket_port" value=5050>
    </form>
    
    <button onclick="redirect_start()">Запуск ceрвера</button>
    
    </div>
    <script>
        function redirect_start() {
            window.location.href = '/choose';
        }
    </script>
</body>
</html>
'''


