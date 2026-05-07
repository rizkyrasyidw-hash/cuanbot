import os
from dotenv import load_dotenv
from telethon import TelegramClient
from mcp.server.fastmcp import FastMCP

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")
CHANNEL = os.getenv("CHANNEL_USERNAME")

client = TelegramClient("session", API_ID, API_HASH)

mcp = FastMCP("Telegram News MCP")

@mcp.tool()
async def get_latest_news(limit: int = 10) -> str:
    """Ambil berita terbaru dari channel Telegram"""
    await client.start(phone=PHONE)
    messages = await client.get_messages(CHANNEL, limit=limit)
    
    result = []
    for msg in messages:
        if msg.text:
            result.append(f"[{msg.date}] {msg.text[:300]}")
    
    await client.disconnect()
    return "\n\n".join(result)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)