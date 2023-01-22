import serial
import json
import matplotlib.pyplot as plt
import keyboard

#połączenie z STM
plt.ion()
hSerial = serial.Serial('COM2', 115200, timeout=1, parity=serial.PARITY_NONE)

#kontorler rozpoczyna pracę
hSerial.reset_input_buffer()
hSerial.flush()

#otworzenie pliku oraz wartości początkowe
file = open("pomiary.txt", "a")
temp_saamples = []
t = []
t_value=0
temperature = 0
sample = 0

while True:
    temp = hSerial.readline()
    try:
        sample = json.loads(temp)
        temperature = sample["temperature"] #odczyt temperatury
        print(temperature)
        file.write("%.2f," % float(temperature))
        temp_saamples.append(float(temperature)) #dodanie odczytu do listy wszystkich temperatur
        #obsługa osi czasu do wykresu
        t.append(t_value)
        t_value = t_value + 1
    except ValueError:
        print("Sth went wrong")
        hSerial.flush()
        hSerial.reset_input_buffer()

    # Plot results
    plt.clf()
    plt.plot(t, temp_saamples, '.', markersize=5)
    plt.title("Temperatura")
    plt.xlabel("Time [s]")
    plt.ylabel("Temperature [C]")
    plt.show()
    plt.pause(0.001)
    if keyboard.is_pressed("q"):
        break

file.close()
hSerial.close()
