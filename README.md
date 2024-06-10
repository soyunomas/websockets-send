# WebSocket File Distribution Server and clients.

This project provides a WebSocket server for distributing files among clients. It allows clients to connect, subscribe to specific topics, and receive files sent by other clients.

### server.py
**Description:** This file implements a WebSocket server for handling file distribution among clients. It listens for incoming WebSocket connections, manages subscriptions to topics, and forwards received files to subscribed clients.

**Usage:** The server can be started using the provided command-line interface (CLI) options to specify the port and IP address to listen on.

**Functionality:**
Listens for WebSocket connections.
Handles incoming messages from clients.
Supports subscription to topics.
Distributes files to clients subscribed to specific topics.
### sender.py
**Description:** This file provides a command-line interface (CLI) for sending files to the WebSocket server. It connects to the server via WebSocket, reads files from the local file system, encodes them as base64, and sends them to the server with the specified topic.

**Usage:** Users can specify the WebSocket URI, topic, and file path as command-line arguments to send files to the server.

**Functionality:**
Establishes a WebSocket connection to the server.
Reads files from the local file system.
Encodes files as base64.
Sends files to the server with the specified topic.

### receive.py
**Description:** This file provides a command-line interface (CLI) for receiving files from the WebSocket server. It connects to the server via WebSocket, listens for incoming messages, and saves received files to the local file system.

**Usage:**
Users can specify the WebSocket URI and topic as command-line arguments to receive files from the server.
**Functionality:**

Establishes a WebSocket connection to the server.
Listens for incoming messages from the server.
Saves received files to the local file system.

### index.html
**Description:** This HTML file contains a simple web interface for interacting with the WebSocket server. It allows users to connect to the server, subscribe to topics, and download files received from the server.

**Usage:** Users can open the HTML file in a web browser to access the web interface.

**Functionality:**
Connects to the WebSocket server using JavaScript.
Allows users to subscribe to topics and download files received from the server.
Provides a user-friendly interface for interacting with the server.

## Usage

To start the WebSocket server, run the following command:

python server.py -p 8765 -i 0.0.0.0

Replace `8765` with the desired port number and `0.0.0.0` with the desired IP address.

## How It Works

- Clients can connect to the server using a WebSocket URI.
- Upon connection, clients can subscribe to specific topics to receive files related to those topics.
- When a client sends a file to a topic, the server distributes the file to all clients subscribed to that topic.
- File messages are formatted as follows: `{mime_type}:{file_name}:{file_data}`.

## Dependencies

- Python 3.x
- asyncio
- websockets
- argparse
