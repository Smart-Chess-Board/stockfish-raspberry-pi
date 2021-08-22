import time
import serial
from stockfish import Stockfish
import os

white = False
black = True
ser = serial.Serial(port='COM3', baudrate=9600)

# need to write a diff wrap function that waits for arduino to send ack
def send(data : str):
    global ser
    ser.write(data.encode())
    ack = ser.readline().decode()
    while (not ack.startswith("ACK")):
        ack = ser.readline().decode()
    print(ack)


def main():
    # initialize stockfish
    laptop_parameters = {
        "Write Debug Log": "false",     # set
        "Contempt": 0,                  # set (could also be 24)
        "Min Split Depth": 0,           # set (should be ok)
        "Threads": 3,                   # set
        "Ponder": "false",              # set
        "Hash": 4,                      # set
        "MultiPV": 1,                   # set
        "Skill Level": 20,              # set (highest skill possible)
        "Move Overhead": 30,            # not too sure
        "Minimum Thinking Time": 20,    # set (this is fine)
        "Slow Mover": 80,               # set (doesn't really matter)
        "UCI_Chess960": "false",        # set
    }
    stockfish = Stockfish("./stockfish/stockfish.exe", depth = 15, parameters = laptop_parameters)
    
    # board set up
    w = input("Is white a player? [y/n] ")
    send(w)
    b = input("Is black a player? [y/n] ")
    send(b)

    turn = white
    isWhiteAI = False if (w == "y" or w == "yes") else True
    isBlackAI = False if (b == "y" or b == "yes") else True

    if (isWhiteAI):
        bestMove = stockfish.get_best_move()
        send(bestMove)

    while (True):
        data = ser.readline().decode()
        print(data)
        if data.startswith("Enter"): # enter event
            event = input()
            if event == "exit":
                return
            send(event)
        elif data[0] == 'M':
            move = data[3:]
            stockfish.make_moves_from_current_position([move])
            turn = not turn

            # send move if required
            if (turn == white and isWhiteAI) or (turn == black and isBlackAI):
                bestMove = stockfish.get_best_move()
                send(bestMove)  

if __name__ == "__main__":
    main()