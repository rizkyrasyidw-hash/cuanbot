import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
from mcp.server.fastmcp import FastMCP

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
CHANNEL = os.getenv("CHANNEL_USERNAME")
PORT = int(os.getenv("PORT", 8000))

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Create FastMCP and configure host/port via constructor (FastMCP.run doesn't accept host/port)
mcp = FastMCP("Telegram News MCP", host="0.0.0.0", port=PORT)

@mcp.tool()
async def get_latest_news(limit: int = 10) -> str:
    """Ambil berita terbaru dari Telegram channel"""
    await client.connect()
    messages = await client.get_messages(CHANNEL, limit=limit)
    
    result = []
    for msg in messages:
        if msg.text:
            date_str = msg.date.strftime("%Y-%m-%d %H:%M")
            result.append(f"[{date_str}] {msg.text[:400]}")
    
    await client.disconnect()
    return "\n\n".join(result) if result else "Tidak ada pesan ditemukan."

if __name__ == "__main__":
    # start the server using StreamableHTTP transport; host/port are configured on the FastMCP instance
    mcp.run(transport="streamable-http")