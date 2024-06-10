"""
WebSocket File Receiver

This program connects to a WebSocket server and receives files sent by clients.

Usage:
  python receive.py -u ws://localhost:8765 -t chat
  python receive.py --uri ws://example.com:8080 --topic files
  python receive.py -u ws://192.168.1.100:9000 -t documents
"""

import asyncio
import websockets
import argparse
import base64
import os

async def receive_files(uri, topic):
    print("Attempting to connect to server...")
    async with websockets.connect(uri) as websocket:
        print(f"Connected to server at {uri} at topic '{topic}'")
        while True:
            print("Waiting for message...")
            message = await websocket.recv()
            print(f"Received message: {message}")
            parts = message.split(":", 2)
            if len(parts) == 3:
                file_name = parts[0]
                file_data = parts[1]
                save_file(file_name, file_data)
                print(f"Received file '{file_name}' from topic '{topic}'")
            else:
                print(f"Received an improperly formatted message: {message}")


def save_file(file_name, file_data):
    with open(file_name, "wb") as file:
        file.write(base64.b64decode(file_data))

def main():
    parser = argparse.ArgumentParser(
        description="WebSocket file receiver",
        epilog=f"""Examples of use:
  python receive.py -u ws://localhost:8765 -t chat
  python receive.py --uri ws://example.com:8080 --topic files
  python receive.py -u ws://192.168.1.100:9000 -t documents""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-u", "--uri", type=str, required=True, help="WebSocket URI (e.g., ws://localhost:8765)")
    parser.add_argument("-t", "--topic", type=str, required=True, help="Topic to subscribe to")

    args = parser.parse_args()

    asyncio.run(receive_files(args.uri, args.topic))

if __name__ == "__main__":
    main()

