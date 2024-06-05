# Интерфейс для передачи файлов

TUNTAP представляет собой удобную утилиту для передачи файлов, которая упрощает процесс отправки данных на удаленный сервер. Она обладает понятным интерфейсом и использует возможности Python для обеспечения надежной передачи файлов.

## Особенности

- Интуитивно понятный GUI: TUNTAP предлагает простой и понятный интерфейс, позволяющий легко вводить информацию о соединении, адрес сервера, порт и выбирать файл для отправки.
- Запуск сценария оболочки для включения необходимого сетевого интерфейса для передачи файлов.
- Выполняет передачу файлов, используя программирование сокетов в Python.
- Позволяет пользователям вводить пароль для команды sudo для запуска сценария оболочки.
- Отображает информацию о передаче файлов и состоянии соединения в графическом интерфейсе.

## Инструкция по установке и настройки для передачи файлов

### Необходимые предустановки для локального хоста
 - Версия интерпретатора Python 3
 - Необходимые библиотеки для корректного запуска:
```sh 
   $sudo pip install pyserial
   $sudo apt install gnome-terminal
```
 - Среда разработки Thonny (по желанию)

### Необходимые предустановки для Raspberry Pi Pico
- Интерпретатор Micropython

### Настройка Rasberry Pi Pico для передачи данных
 1. Клонируйте этот репозиторий с помощью `git clone` в удобное место.
 2. Подключите плату к компьютеру и убедитесь, что операционная система ее распознала. Вы можете проверить с помощью команды:
   
```sh 
    $ ls /dev/ttyACM*
    ttyACM0
```
 4. С помощью среды разработки Thonny откройте (или создайте) файл `main.py`.
 5. Скопируйте код из папки `firmware_for_pico` из файла `main_for_pico.py`.
 6. Сохраните изменения, перезапустите плату.
 7. Повторите с пункта 1 для второй платы.
 8. Подключение проводов в UART: tx (pin0) - rx (pin1) для контактов платы, которые являются соответственно 1-м и 2-м контактами.
 ![Подключение Raspberry Pi Pico](/firmware_for_pico/Pico_connect.jpg)

### Настройка TAP интерфейса
1. Запустите исполняемый файл `run.sh`.
2. После успешного запуска должно открыться новое окно с надписью "Для настройки интерфейса TAP перейдите в браузер по адресу: http://localhost:7070".
3. Перейдите по указанному адресу в интернет-браузере.
![Вид TAP интерфейса](/socket_file/Tap_manager_interface.png)
4. Введите необходимую информацию в поля для настройки и запуска интерфейса TAP:
   - Введите свой системный пароль для запуска сценария оболочки с привилегиями sudo.
   - IP-адрес источника и IP-адрес назначения используются для настройки маршрутизации этого интерфейса.    
     Следовательно, на другом компьютере необходимо зеркально поменять адреса для успешного соединения
   - После ввода данных и нажатия кнопки "Запуск интерфейса TAP" должно открыться окно терминала с данными в реальном времени.    
     Это означает, что интерфейс успешно нашел последовательный порт и записывает с системного стека TCP/IP в него данные.

### Настройка сокет-сервера
 - После запуска интерфейса TAP возможно прослушивание его с помощью сокет-сервера. 
 - Для этого перейдите на вкладку "Сокет-сервер" в браузере и укажите IP-адрес интерфейса TAP и выберите удобный порт.  
 - После нажатия кнопки "Запуск сервера" должно открыться новое окно с терминалом с успешным запуском. "Server listen ('ваш введенный ip адрес интерфейса', порт)"

### Настройка сокет-клиента
 - После успешного запуска сервера, клиент запускается на другой стороне передачи.  
   Соответственно необходимо установить и запустить TAP интерфейс с зеркально прописанным ip от другой стороны перед настройкой клиента 
 - После запуска TAP интерфейса, переходим во вкладку "Socket client" и вводим ip адрес сервера на который ходим передать данные.
 - Укажите имя файла, который вы хотите передать.
  Клиент учитывает только файлы из папки `socket_files`. Если файл с указанным именем там не обнаружен, клиент сообщит об ошибке.


## Структура кода
- HTML: Используется для создания интерфейсов.
- Модуль Python's socket: Обеспечивает передачу файлов.
- Модуль subprocess: Запускает сценарий оболочки.
- Функция Struct pack: Форматирует длину файла.
- Последовательный порт Serial: Обеспечивает связь между Pico и компьютером.

## Лицензия

TUNTAP выпускается под лицензией MIT.

## Отказ от ответственности

Хотя TUNTAP нацелен на облегчение передачи файлов между локальной машиной и удаленным сервером, важно обеспечить надлежащие меры безопасности. Это включает в себя правильную настройку удаленного сервера и сетевых параметров, а также защиту конфиденциальной информации во время процесса передачи. Используйте TUNTAP на свой страх и риск и всегда учитывайте последствия для безопасности при передаче файлов по сети.
