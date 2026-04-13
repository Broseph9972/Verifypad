import serial
import time
import threading

conn = None
messageHandler = None
shouldLog = False

def init(port, onMessage, log=True):
    global conn, messageHandler, shouldLog
    if conn and conn.is_open:
        return False
    try:
        conn = serial.Serial(port, 9600, timeout=1)
    except Exception as e:
        print(f"Error: {e}")
        return False
    messageHandler = onMessage
    shouldLog=log
    threading.Thread(target=start_monitoring, daemon=True).start()
    return True

def start_monitoring():
    global conn
    while True:
        if conn and conn.is_open:
            try:
                if conn.in_waiting > 0:
                    data = conn.read(conn.in_waiting)
                    messageHandler(data)
                    if shouldLog:
                        print(f"Received: {data}")
            except Exception as e:
                print(f"Error: {e}")
                break
        else:
            break
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
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    return False