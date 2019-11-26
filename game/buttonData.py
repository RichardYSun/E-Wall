import serial


class Button:
    def __init__(self, buttonID, state):
        self.buttonID = buttonID
        self.state = state


def send(button, state) -> Button:
    curButton = Button(button, state)
    return curButton


controller_connected = False
try:
    arduino = serial.Serial('COM3', timeout=1, baudrate=9600)
    controller_connected = True
except serial.SerialException:
    pass


# Sift through data received from serial

def button():
    if not controller_connected:
        return None
    newData = (arduino.readline())
    dataDecode = newData.decode("utf-8")
    splitWork = True
    button = None
    state = None
    split = None
    try:
        split = dataDecode.split(",")
    except:
        splitWork = False

    if splitWork == True:
        button = int(split[0])
        state = int(split[1])

    return send(button, state)

# while True:
#   data = (arduino.readline())

#  try:
#      print(data.decode("utf-8"))
#    except:
#        print(data + "Fail")

#    splitWork = True
#    try:
#        split = data.split(",")
#   except:
#       splitWork = False
#   if splitWork:
#       button = int(split[0])
#       state = int(split[1])
#       send(button, state)


# split = data.split(",")
# button = int(split[0])
# state = int(split[1])
# send(button, state)
