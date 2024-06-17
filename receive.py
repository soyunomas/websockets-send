"""
WebSocket File Receiver

This program connects to a WebSocket server and receives files sent by clients.

Usage:
  python receive.py -u ws://localhost:8765 -t chat
  python receive.py --uri ws://example.com:8080 --topic files
  python receive.py -u ws://192.168.1.100:9000 -t documents
"""

import asyncio
import argparse
import base64
import os
from config import max_size  # Import the max_size from the config file

try:
  import websockets
except ImportError:
  print("Error: The 'websockets' library is not installed.")
  print("Please install it using 'pip install websockets'.")
  exit(1)

async def receive_files(uri, topic):
    print("Attempting to connect to server...")

    async with websockets.connect(uri, max_size=max_size) as websocket:
        print(f"Connected to server at {uri}")
        await websocket.send(f"subscribe:{topic}")
        print(f"Subscribed to topic: {topic}")
        
        while True:
            print("Waiting for message...")
            message = await websocket.recv()
 #          print(f"Received message: {message}")
            parts = message.split(":", 4)
 #          print(f"Message parts: {parts}")

            if len(parts) == 3:
                mime_type = parts[0]
                file_name = parts[1]
                file_data = parts[2]
                save_file(file_name, file_data)
                print(f"Received file '{file_name}' from topic '{topic}' with MIME type '{mime_type}'")
            else:
                print(f"Received an improperly formatted message: {message}")

def save_file(file_name, file_data):
    file_data_decoded = base64.b64decode(file_data)
    with open(file_name, "wb") as file:
        file.write(file_data_decoded)
    print(f"File '{file_name}' saved successfully.")

def main():
    parser = argparse.ArgumentParser(
        description="WebSocket file receiver",
        epilog=f"""Examples of use:
  python receive.py -u ws://localhost:8765 -t chat
  python receive.py --uri ws://example.com:8080 --topic files
  python receive.py -u ws://192.168.1.100:9000 --topic documents""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-u", "--uri", type=str, required=True, help="WebSocket URI (e.g., ws://localhost:8765)")
    parser.add_argument("-t", "--topic", type=str, required=True, help="Topic to subscribe to")

    args = parser.parse_args()

    asyncio.run(receive_files(args.uri, args.topic))

if __name__ == "__main__":
    main()

