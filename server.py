import os
import logging
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
CHANNEL = os.getenv("CHANNEL_USERNAME")
PORT = int(os.getenv("PORT", 8000))

logger.info("Starting Telegram MCP Server...")

if not all([API_ID, API_HASH, SESSION_STRING, CHANNEL]):
    logger.error("❌ Missing required environment variables!")
    exit(1)

mcp = FastMCP("Telegram News MCP")

@mcp.tool()
async def get_latest_news(limit: int = 10) -> str:
    """Ambil berita terbaru dari channel Telegram"""
    client = TelegramClient(StringSession(SESSION_STRING), int(API_ID), API_HASH)
    try:
        await client.connect()
        messages = await client.get_messages(CHANNEL, limit=limit)
        
        result = []
        for msg in messages:
            if msg.text:
                date_str = msg.date.strftime("%Y-%m-%d %H:%M")
                result.append(f"[{date_str}] {msg.text[:400]}")
        
        return "\n\n".join(result) if result else "Tidak ada berita."
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"Error: {str(e)}"
    finally:
        await client.disconnect()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        mcp.sse_app(), 
        host="0.0.0.0", 
        port=PORT,
        log_level="info"
    )