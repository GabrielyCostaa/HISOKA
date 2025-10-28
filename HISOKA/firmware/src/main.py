

from radio.receiver import Receiver
from radio.sender import Sender
from config import files

def FactoryDevice(receiver):

    def create_receiver():
       return Receiver(queue_size=1000)

    def create_sender():
       return Sender(range=100)
    
    device = create_receiver() if receiver else  create_sender()
    device.init()

    return device

if __name__ == "__main__":
    try:
        RECEIVER = files.has_config("receiver")
        device = FactoryDevice(RECEIVER)

        
        for task in device.get_async():
            device.loop.create_task(task())

        device.loop.run_forever()

    except KeyboardInterrupt:
        print("Program stopped.")