import websockets
import asyncio
import threading
import os
import json
from utils.Config import ConfigDeviceInfo

class Client(threading.Thread): 
    def __init__(self, host="localhost", port=8000):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.consumer_handler = self.handle_websocket_receive
        self.producer_handler = self.handle_websocket_send
        self.is_websocket_connected = False
        self.config = ConfigDeviceInfo()
        
    def run(self):
        asyncio.run(self.start_connection())
    
    
    async def start_connection(self):
        async with websockets.connect(f"ws://{self.host}:{self.port}") as websocket:
            while True:
                await asyncio.gather(
                    self.consumer_handler(websocket),
                    self.producer_handler(websocket),
                )
                
    @staticmethod            
    async def handle_websocket_receive(ws):
        try:
            incoming_json = await asyncio.wait_for(ws.recv(), 10)
            incoming = json.loads(incoming_json)
            
            if incoming["cmd"] == "START":
                print("[WEBSOCKET] INICIANDO MEDIÇÃO")
                os.environ["START_READINGS"] = "True"
                os.environ["N_READINGS"] = str(incoming["num_medicao"])
                os.environ["INTERVALO"] = str(incoming["intervalo"])
                
            if incoming["cmd"] == "PAUSE":
                print("[WEBSOCKET] MEDIÇÃO PAUSADA")
                os.environ["PAUSE"] = "True"

            if incoming["cmd"] == "STOP":
                print("[WEBSOCKET] MEDIÇÃO FINALIZADA PELO USUáRIO")
                os.environ["START_READINGS"] = "False"
                os.environ["PAUSE"] = "False"
                os.environ["N_READINGS"] = "0"

            if incoming["cmd"] == "RESTART":
                print("[WEBSOCKET] MEDIÇÃO RENICIADA")
                os.environ["PAUSE"] = "False"

        except:
            pass

    async def handle_websocket_send(self, ws):
        payload = {"device": "standard", "cmd": ""}
        start = os.environ["START_READINGS"] == "True"
        if not self.is_websocket_connected:
            payload["cmd"] = {
            "id": self.config.id,
            "location": self.config.location,
            "type": self.config.type,   
            "model": "Raspberry pi 3B+",
            "version": "Raspbian GNU/Linux 10 (buster)"           
            }
            self.is_websocket_connected = True
            await ws.send(json.dumps(payload))
        elif start and int(os.environ["N_READINGS"]) > 0:
            payload["cmd"] = f"Percentual da calibração: {self.calibration_percent(int(os.environ['N_READINGS']))}"
            await ws.send(json.dumps(payload))

    @staticmethod 
    def calibration_percent(n_readings):
        total_measures = int(os.environ['TOTAL_MEASURES_COUNTER'])
        return (total_measures / (n_readings * int(os.environ['NUMBER_OF_PROPERTIES']))) * 100
        
