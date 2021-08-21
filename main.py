import time
import serial


def main():
    ser = serial.Serial(port='COM3', baudrate=9600)
    start = time.time()
    while (True):
        data = ser.readline().decode()
        if data[0] == 'M':
            move = data[3:]
            print(move)
        if time.time() - start > 10:
            return

if __name__ == "__main__":
    main()