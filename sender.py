"""
WebSocket File Sender

This program connects to a WebSocket server and sends a file over the connection.
It encodes the file data to base64 before sending it.

Usage:
  python sender.py -u ws://localhost:8765 -t chat -f /path/to/file.txt
  python sender.py --uri ws://example.com:8080 --topic files --file_path /path/to/image.png
  python sender.py -u ws://192.168.1.100:9000 -t documents -f /path/to/document.pdf
"""

import asyncio
import websockets
import argparse
import base64
import os
import sys
from config import max_size  # Import the max_size from the config file

async def send_file(uri, topic, file_path):
    # Obtain the file size
    file_size = os.path.getsize(file_path)
    
    # Configure the progress bar
    bar_length = 40
    sys.stdout.write(f"Sending: [{' ' * bar_length}] 0/{file_size} bytes\r")
    sys.stdout.flush()

    async with websockets.connect(uri, max_size=max_size) as websocket:

        # Read the file and encode it to base64
        with open(file_path, "rb") as file:
            file_data = base64.b64encode(file.read()).decode()

        # Get the MIME type and file name
        mime_type = "application/octet-stream"
        file_name = os.path.basename(file_path)

        # Send the file to the server in the correct format
        message = f"message:{topic}:{mime_type}:{file_name}:{file_data}"
        await websocket.send(message)
        print(f"Sent file {file_name} to topic {topic} on {uri}        ")

def main():
    parser = argparse.ArgumentParser(
        description="WebSocket file sender",
        epilog=f"""Examples of use:
  python sender.py -u ws://localhost:8765 -t chat -f /path/to/file.txt
  python sender.py --uri ws://example.com:8080 --topic files --file_path /path/to/image.png
  python sender.py -u ws://192.168.1.100:9000 -t documents -f /path/to/document.pdf""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-u", "--uri", type=str, required=True, help="WebSocket URI (e.g., ws://localhost:8765)")
    parser.add_argument("-t", "--topic", type=str, required=True, help="Topic to send the file to")
    parser.add_argument("-f", "--file_path", type=str, required=True, help="Path of the file to send")

    args = parser.parse_args()

    asyncio.run(send_file(args.uri, args.topic, args.file_path))

if __name__ == "__main__":
    main()

