import asyncio
import websockets
import json

async def simulate_chat(user_id):
    uri = "ws://localhost:8000/ws/chat/user1/user2/"  # Adjust the WebSocket path accordingly

    async with websockets.connect(uri) as websocket:
        while True:
            message = input(f"User {user_id} - Enter message: ")
            data = {
                "receiver": "user2",  # Adjust the receiver user ID accordingly
                "message": message,
            }
            await websocket.send(json.dumps(data))

async def main():
    # Adjust the number of simulated users as needed
    users = ["user1", "user2"]

    tasks = [simulate_chat(user_id) for user_id in users]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
