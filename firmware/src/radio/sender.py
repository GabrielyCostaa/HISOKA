from radio.espnow_comm import ESPNOW_BASE
from primitives.queue import Queue
import asyncio
from machine import ADC, PWM, Timer
import time, struct

PKG_SIZE = 62
MAX_STORAGE = 100
from machine import freq

class Sender(ESPNOW_BASE):
    def __init__(self, range=100, colect_freq=2_000, mvs_widow=4):
        super().__init__()
        freq(240000000)
        self.receiver_mac = None
        self.range = range
        self.data = Queue(100) #2x Max_freq?
        self.pin = ADC(2)
        self.pin.atten(ADC.ATTN_11DB)
        self.pin.width(ADC.WIDTH_12BIT)
        self.clk = PWM(1, freq=500, duty_u16=32768)
        self.clk.init()
        self.index = 0
        self.data_pack = []
        self.DATA_FREQ = round(colect_freq/PKG_SIZE)*PKG_SIZE
        print(self.DATA_FREQ)
        self.MVS_WINDOW = mvs_widow
        self.raw_data = [0]*self.MVS_WINDOW
        self.mvs_data = [ ]
        self.storage = [ ]
        
        self.data_flag = asyncio.ThreadSafeFlag()
    
    def init_Timers(freqs, clbks):
        for idx, (freq, clbk) in enumerate(zip(freqs, clbks)):
            timer = Timer(idx)
            timer.init(mode=Timer.PERIODIC, freq=freq, callback=clbk)
    
    def read_data_clbk(self, timer):
        storage = self.storage
        raw_data = self.raw_data
        mvsw = self.MVS_WINDOW
        if len(self.mvs_data) >= PKG_SIZE:
            if len(storage) < MAX_STORAGE:
                # print("add to storage", len(storage))
                self.storage.append(self.mvs_data.copy())
                self.mvs_data.clear()
                # self.storage = storage
            self.data_flag.set()
            # return
        else:
            raw_data.append(self.pin.read_uv())
            raw_data.pop(0)
            self.mvs_data.append(sum(raw_data[:mvsw])/mvsw)
            self.raw_data = raw_data
            self.storage = storage


    async def listen_for_receiver(self):
        """Listen for broadcast messages from the receiver containing its MAC address."""
        while not self.receiver_mac:
            async for sensor_host, msg in self.esp:
                if self.receiver_mac != sensor_host:
                    self.receiver_mac = sensor_host
                    self.esp.add_peer(sensor_host)
                    Sender.init_Timers(
                        [self.DATA_FREQ],
                        [self.read_data_clbk]
                    )
                    print(f"Receiver MAC registered {sensor_host} {msg}")
            await asyncio.sleep(0)


    async def send_data(self):
        """Send sensor data to the registered receiver."""
        while True:
            if not self.receiver_mac:
                await asyncio.sleep(5)
            else:
                await self.data_flag.wait()
                if len(self.storage)>0:
                    dpkg = self.storage.pop()
                    for i in dpkg:
                        send_ok = False
                        while not send_ok:
                            send_ok = await self.esp.asend(self.receiver_mac, f"{time.ticks_ms()}:{i}".encode("utf-8"))
                    self.data_flag.clear()
                await asyncio.sleep(0)

    def get_async(self):
        return self.listen_for_receiver, self.send_data