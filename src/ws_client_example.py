import asyncio
import websockets
import json
import argparse
import sys

async def subscribe_to_activities(uri):
    """
    Subscribes to activity updates via WebSocket.
    """
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected! Waiting for updates...")
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                print(f"\n[EVENT] {data.get('type')}")
                if data.get('type') == 'signup':
                    print(f"  Student {data.get('email')} signed up for {data.get('activity')}")
                    print(f"  Availability: {data.get('participants_count')}/{data.get('max_participants')}")
                elif data.get('type') == 'unregister':
                    print(f"  Student {data.get('email')} unregistered from {data.get('activity')}")
                    print(f"  Availability: {data.get('participants_count')}/{data.get('max_participants')}")
                elif data.get('type') == 'activity_created':
                    print(f"  New activity created: {data.get('name')}")
                    print(f"  Description: {data.get('details', {}).get('description')}")
                elif data.get('type') == 'activity_updated':
                    print(f"  Activity updated: {data.get('name')}")
                else:
                    print(f"  Data: {json.dumps(data, indent=2)}")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by server.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subscribe to activity updates")
    parser.add_argument("--uri", default="ws://localhost:8000/ws", help="WebSocket URI")
    args = parser.parse_args()

    try:
        asyncio.run(subscribe_to_activities(args.uri))
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
