import websockets
import asyncio
import threading

class Client(threading.Thread): 
    def __init__(self, consumer_handler, producer_handler, host="localhost", port=8000):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.consumer_handler = consumer_handler
        self.producer_handler = producer_handler
        
    def run(self):
        asyncio.run(self.start_connection())
    
    async def start_connection(self):
        async with websockets.connect(f"ws://{self.host}:{self.port}") as websocket:
            while True:
                await asyncio.gather(
                    self.consumer_handler(websocket),
                    self.producer_handler(websocket),
                )
