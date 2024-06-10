"""
WebSocket File Server

This program listens for WebSocket connections and handles file distribution among clients.

Usage:
  python server.py -p 8765 -i 0.0.0.0
"""

import asyncio
import websockets
import argparse
from collections import defaultdict

clients = defaultdict(set)

async def handler(websocket, path):
    """
    Handle WebSocket connections and messages.
    
    Args:
        websocket: The WebSocket connection object.
        path: The path requested by the client.
    """
    print(f"Client connected from {websocket.remote_address}")
    async for message in websocket:
        if message.startswith("subscribe:"):
            topic = message.split(":")[1]
            clients[topic].add(websocket)
            try:
                async for _ in websocket:
                    pass
            finally:
                clients[topic].remove(websocket)
        elif message.startswith("message:"):
            parts = message.split(":", 4)
            if len(parts) == 5:
                topic = parts[1]
                mime_type = parts[2]
                file_name = parts[3]
                file_data = parts[4]
                print(f"Received file '{file_name}' on topic '{topic}'")             
                for client in clients[topic]:    
                    await client.send(f"{mime_type}:{file_name}:{file_data}")
            else:
                print(f"Received an improperly formatted message: {message}")

def main():
    parser = argparse.ArgumentParser(description="WebSocket server for file distribution")
    parser.add_argument("-p", "--port", type=int, default=8765, help="Port to listen on (default: 8765)")
    parser.add_argument("-i", "--ip", type=str, default="0.0.0.0", help="IP address to listen on (default: 0.0.0.0)")

    args = parser.parse_args()

    start_server = websockets.serve(handler, args.ip, args.port)

    print(f"Server listening on {args.ip}:{args.port}")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()

