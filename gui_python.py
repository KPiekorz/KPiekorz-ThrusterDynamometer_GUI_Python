
from func_class import *
import threading


class DisplayMenu(threading.Thread):
    def __init__(self, id, name):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name

    def run(self):
        print("Alikacja obslugi hamowni")
        while True:
            print("Komendy:\n0 - Stop (zatrzymuje wszystko);\n1 - Start (rozpoczyna pomiary z czujnikow, uruchamia pwm do silnika);\n3 - Zmiana predkosci silnika (0 - 100);\n4 - Zapis pomiarow z czujnikow;")
            wybrana_komenda = input("Wybierz komende: ")
            # if wybrana_komenda[0] == '3' or wybrana_komenda[0] == '4':
            #     parametr = wybrana_komenda[2:]
            # else:
            #     parametr = 0
            switch = Switcher()
            # print(switch.numbers_to_methods_to_strings(wybrana_komenda[0], int(parametr)))
            print(switch.numbers_to_methods_to_strings(wybrana_komenda, 0))
            print("\n")


if __name__ == "__main__":

    # LOCAL_HOST = '127.0.0.1'
    # HOST = '169.254.57.55'
    # PORT = 80
    #
    #
    # start_command = b'[1|1|1|1|1]'
    # stop_command = b'[0|0|0|0|0]'
    #
    #
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT))
    #     s.send(start_command)
    #     # time.sleep(1)
    #
    #     for i in range(4000):
    #         rcv = s.recv(80)
    #         print(rcv)
    #
    #     s.send(stop_command)
    #
    #     s.close()

    thread_cmd = DisplayMenu(1, "CMD Thread")
    thread_rcv = ReceiveFrame(2, "Rcv Thread")

    thread_cmd.start()
    thread_rcv.start()

    thread_cmd.join()
