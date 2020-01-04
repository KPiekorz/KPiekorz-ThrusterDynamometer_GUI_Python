import re


def time_to_sec(min, sec, milis):
    milis_to_sec = milis/1000
    min_to_sec = min*60
    return min_to_sec+sec+milis_to_sec


def make_dict_from_frame(frame):
    field_values = re.findall(r"[\.\w']+", frame)
    # zamieniamy liczby na int
    field_values = list(map(float, field_values))
    time = time_to_sec(min=field_values[0], sec=field_values[1], milis=field_values[2])
    temp = field_values[3:5]
    press = field_values[5]
    vibro_table = field_values[6:16]
    shunt = field_values[16]
    hal_table = field_values[17:27]
    tenso = field_values[27]

    field_values = []
    field_values.append(time)
    field_values.append(temp)
    field_values.append(press)
    field_values.append(vibro_table)
    field_values.append(shunt)
    field_values.append(hal_table)
    field_values.append(tenso)
    print(field_values)

    field_names = ['Time', 'Temperature', 'Pressure', 'Vibration', 'Shunt', 'Hal', 'Tensometer']
    return dict(zip(field_names, field_values))


def read_frame_from_file():
    '''tworz pliki z podzialem na wyniki z poszczegolnych czujnikow'''
    f = open("Data_dumps/moje_wyniki.txt", "r")

    f1 = f.readlines()
    print(f1[1])
    dict_frame = make_dict_from_frame(f1[1])
    print(dict_frame['Time'])

    f.close()


read_frame_from_file()
