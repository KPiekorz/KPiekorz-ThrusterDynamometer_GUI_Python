import socket
import threading

# HOST = '127.0.0.1'
# PORT = 1234
HOST = '169.254.57.55'
PORT = 80

event = threading.Event()
event.clear()


class Switcher(object):
    def numbers_to_methods_to_strings(self, argument, parametr):
        """Dispatch method"""
        # prefix the method_name with 'number_' because method names
        # cannot begin with an integer.
        method_name = 'number_' + argument
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "nothing")
        # # Call the method as we return it
        return method()

    def number_0(parametr):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(b'[0|0|0|0|0]')
            s.close()
        return "Zatrzymano prace hamowni!!!"

    def number_1(parametr):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(b'[1|0|0|0|0]')
            s.close()
        return "Jazda Jazda!!!"

    def number_2(parametr):
        return "two"

    def number_3(parametr):
        return "Ustawiono nowa wartosc PWM"

    def number_4(parametr):
        event.set()
        return "Zapis rozpoczety"


class ReceiveFrame(threading.Thread):
    def __init__(self, id, name):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name

    def run(self):
        while True:
            event.wait()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                with open('wyniki.txt', 'w') as f:
                    for i in range(4000):
                        rcv_frame = s.recv(80)
                        rcv_frame = rcv_frame.decode("utf-8")
                        rcv_frame += '\n'
                        f.write(rcv_frame)
                    f.close()
                s.close()
            event.clear()
