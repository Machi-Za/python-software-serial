import serial, serial.tools.list_ports
from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread, Event

class Ports(QObject):
    ReadExisting = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        # Initialize the serial port with default settings
        self.serial = serial.Serial()
        self.serial.timeout = 0.5            
        self.thread = None
        self.alive = Event()        
        self.PortName = [port.device for port in serial.tools.list_ports.comports()]
        self.BaudRate = ["300","1200","2400","4800","9600","19200","38400","57600","48800","115200","230400","250000","1000000","2000000"]

    # Open the serial port and start the read thread
    def Open(self):
        self.serial.open()
        if(self.serial.is_open):
            self.start_thread()

    # Close the serial port and stop the read thread
    def Close(self):
        self.stop_thread()
        self.serial.close()

    # Read data from the serial port
    def Read(self):
        while (self.alive.isSet() and self.serial.is_open):
            data = self.serial.readline().decode("utf-8", errors="ignore").strip()

            if data:
                self.ReadExisting.emit(data)
    
    # Write data to the serial port
    def Write(self, data):
        if(self.serial.is_open):
            messages = str(data) + "\n"
            self.serial.write(messages.encode())

    # Start the read thread
    def start_thread(self):
        self.thread = Thread(target = self.Read)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()
    
    # Stop the read thread
    def stop_thread(self):
        if(self.thread is not None):
            self.alive.clear()
            self.thread.join()
            self.thread = None