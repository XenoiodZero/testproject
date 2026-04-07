"""
RAG AI Discord Bot — main entrypoint.
Loads knowledge base, connects to Discord, registers slash commands from commands.py.
"""

import os
import time
from types import SimpleNamespace

import discord
from discord import app_commands
from dotenv import load_dotenv

from vector_store import VectorStore
from llm_client import ClaudeClient
from commands import setup_commands

load_dotenv()

# --- Config ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-6")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

BOT_VERSION = "0.3.0"
BOT_AUTHORS = "XenoiodZero"
BOT_TOOLS = (
    "Python, discord.py, FAISS, sentence-transformers, "
    "Anthropic Claude API, python-dotenv"
)
START_TIME = time.time()

# --- Init components ---
print("[Bot] Loading vector store...")
vector_store = VectorStore(embedding_model=EMBEDDING_MODEL)
vector_store.load_documents("knowledge_base")
vector_store.build_index()

print("[Bot] Initializing Claude client...")
llm = ClaudeClient(api_key=ANTHROPIC_API_KEY, model=CLAUDE_MODEL)

# --- Discord bot ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

ctx = SimpleNamespace(
    client=client,
    llm=llm,
    vector_store=vector_store,
    model=CLAUDE_MODEL,
    version=BOT_VERSION,
    authors=BOT_AUTHORS,
    tools_str=BOT_TOOLS,
    start_time=START_TIME,
)
setup_commands(tree, ctx)


@client.event
async def on_ready():
    print(f"[Bot] Logged in as {client.user}")
    print(f"[Bot] Knowledge base: {vector_store.index.ntotal} indexed chunks")
    print(f"[Bot] Using model: {CLAUDE_MODEL}")
    try:
        synced = await tree.sync()
        print(f"[Bot] Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"[Bot] Failed to sync slash commands: {e}")


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("ERROR: DISCORD_TOKEN not set. Copy .env.example to .env and fill it in.")
        exit(1)
    if not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set. Get one at https://console.anthropic.com/")
        exit(1)

    client.run(DISCORD_TOKEN)
