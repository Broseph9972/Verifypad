import serial
import time
import threading

conn = None
messageHandler = None
closeHandler = None
shouldLog = False

def _notify_close():
    global conn
    conn = None
    if closeHandler:
        closeHandler()

def init(port, onMessage, onClose, log=True):
    global conn, messageHandler, shouldLog, closeHandler
    if conn and conn.is_open:
        return False
    try:
        conn = serial.Serial(port, 9600, timeout=1)
    except Exception as e:
        print(f"Error: {e}")
        return False
    messageHandler = onMessage
    closeHandler = onClose
    shouldLog=log
    threading.Thread(target=start_monitoring, daemon=True).start()
    return True

def start_monitoring():
    global conn
    while True:
        if conn and conn.is_open:
            try:
                if conn.in_waiting > 0:
                    data = conn.read(conn.in_waiting).decode("utf-8")
                    if shouldLog:
                        print(f"Received: {data}")
                    messageHandler(data)
            except Exception as e:
                print(f"Error: {e}")
                _notify_close()
                return
        else:
            _notify_close()
            return
        time.sleep(0.1)

def sendMessage(msg):
    if conn and conn.is_open:
        conn.write(msg.encode("utf-8"))
        return True
    else:
        return False

def closeConnection():
    global conn
    if conn and conn.is_open:
        try:
            conn.close()
            _notify_close()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    return False