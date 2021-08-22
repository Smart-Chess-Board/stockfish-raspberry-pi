import time
import serial


def main():
    ser = serial.Serial(port='COM3', baudrate=9600)
    while (True):
        data = ser.readline().decode()
        print(data)
        if data.startswith("Enter"): # enter event
            event = input()
            if event == "exit":
                return
            ser.write(event.encode())
        elif data[0] == 'M':
            move = data[3:]
            print("Received: ", move)

if __name__ == "__main__":
    main()