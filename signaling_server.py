import asyncio, websockets, json

clients = {}
async def handler(ws, path):
    client_id = None
    try:
        async for msg in ws:
            data = json.loads(msg)
            action = data.get("action")
            if action == "register":
                client_id = data["clientId"]
                clients[client_id] = ws
            elif action in ("offer", "answer", "ice"):
                target = data.get("targetId")
                if target in clients:
                    await clients[target].send(json.dumps(data))
    except: pass
    finally:
        if client_id and client_id in clients:
            del clients[client_id]

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000):
        await asyncio.Future()

asyncio.run(main())
