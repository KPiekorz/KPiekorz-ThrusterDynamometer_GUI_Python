import threading
import socket
from file_operations import read_frame_from_file


HOST = '127.0.0.0'
PORT = 1234
# HOST = '169.254.57.55'
# PORT = 80

event = threading.Event()
event.clear()

###################################################################################################################################


class Switcher(object):
    def numbers_to_methods_to_strings(self, argument, parametr):
        method_name = 'number_' + argument
        method = getattr(self, method_name, lambda: "nothing")
        return method()

    def number_0(parametr):     # zatrzymuje prace hamowni
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(b'[0|0|0|0|0]')
            s.close()
        return "Zatrzymano prace hamowni!!!"

    def number_1(parametr):     # rozpoczna prace hamowni
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(b'[1|0|0|0|0]')
            s.close()
        return "Jazda Jazda!!!"

    def number_2(parametr):     # zmiania predkosci silnia
        return "two"

    def number_3(parametr):     # zapis danych z czujikow - uruchomienie tasku ReceiveFrame
        return "Ustawiono nowa wartosc PWM"

    def number_4(parametr):     # podzielenie danych na czytelne do matlaba
        event.set()
        return "Zapis rozpoczety"

    def number_5(parametr):     # zakonczenie pracy aplikacji
        pass

    def number_6(parametr):     # wybranie trybu pracy aplikacji
        pass


###################################################################################################################################


class ThreadCmd(threading.Thread):
    def __init__(self, id, name, i):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.i = i

    def run(self):
        print("Alikacja obslugi hamowni")
        while True:
            print("""
Komendy:\n
0 - Stop (zatrzymuje wszystko);
1 - Start (rozpoczyna pomiary z czujnikow, uruchamia pwm do silnika);
2 - Zmiana predkosci silnika;
3 - Zapis pomiarow z czujnikow;
4 - Przerobienie na dane do matlab;
5 - Zakonczenie pracy aplikacji;
6 - Uruchomienie trybu pracy hamowni;
                  """)
            wybrana_komenda = input("Wybierz komende: ")
            switch = Switcher()
            print(switch.numbers_to_methods_to_strings(wybrana_komenda, 0))
            print("\n")


class ThreadReceiveFrame(threading.Thread):
    def __init__(self, id, name, i):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.i = i

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


class ThreadFileOperations(threading.Thread):
    def __init__(self, id, name, i):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.i = i

    def run(self):
        pass


class ThreadPlot(threading.Thread):
    def __init__(self, id, name, i):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.i = i

    def run(self):
        pass


###################################################################################################################################


if __name__ == "__main__":
    threadcmd = ThreadCmd(1, "First Thread", 1)
    threadreceiveframe = ThreadReceiveFrame(2, "Second Thread", 2)
    threadfileoperations = ThreadFileOperations(3, "Third Thread", 3)

    threadcmd.start()
    threadreceiveframe.start()
    threadfileoperations.start()

    threadcmd.join()
    threadreceiveframe.join()
    threadfileoperations.join()
