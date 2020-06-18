import serial
from serial.tools import list_ports
from util import set_dialog

class SerialController(object):
    def __init__(self, parent):
        super(SerialController, self).__init__()
        self.console = parent.GetPane("Console").window
        self.selected_serial = None
        self.ports = self.getPorts()
        self.bauds = []

    def getPorts(self):
        ports = []

        for n, (portname, desc, hwind) in enumerate(sorted(list_ports.comports())):
            ports.append(portname)
        return ports

    def getBaudRates(self):
        if self.selected_serial:
            standard = [9600, 19200, 38400, 57600, 115200]
            return standard[:standard.index(self.selected_serial.baudrate) + 1]

    def setCurrentSerial(self, port):
        self.selected_serial = serial.Serial(port)
        self.selected_serial.close()
        self.bauds = self.getBaudRates()

    def sendCommand(self, cmd):
        if self.selected_serial:
            self.selected_serial.write(cmd + '\n')
            response = self.selected_serial.readlines()
            self.console.print(response)
        else:
            set_dialog("Please connect to port to send commands.")