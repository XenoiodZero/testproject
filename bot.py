"""
RAG AI Discord Bot
Main entrypoint — loads knowledge base, connects to Discord, handles messages.
"""

import os
import discord
from dotenv import load_dotenv
from vector_store import VectorStore
from llm_client import LLMClient

load_dotenv()

# --- Config ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/llama-3-8b-instruct:free")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
BOT_PREFIX = "!ask"

# --- Init components ---
print("[Bot] Loading vector store...")
vector_store = VectorStore(embedding_model=EMBEDDING_MODEL)
vector_store.load_documents("knowledge_base")
vector_store.build_index()

print("[Bot] Initializing LLM client...")
llm = LLMClient(api_key=OPENROUTER_API_KEY, model=LLM_MODEL)

# --- Discord bot ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"[Bot] Logged in as {client.user}")
    print(f"[Bot] Knowledge base: {vector_store.index.ntotal} indexed chunks")
    print(f"[Bot] Using model: {LLM_MODEL}")


@client.event
async def on_message(message: discord.Message):
    # Ignore own messages
    if message.author == client.user:
        return

    # Only respond to !ask commands
    if not message.content.startswith(BOT_PREFIX):
        return

    question = message.content[len(BOT_PREFIX):].strip()
    if not question:
        await message.reply("Please ask a question! Example: `!ask What is RAG?`")
        return

    # Show typing indicator while processing
    async with message.channel.typing():
        # Retrieve relevant context
        results = vector_store.query(question, top_k=3)

        # Generate response
        answer = llm.generate(question, results)

        # Add source info if we got hits
        if results:
            sources = set(r["source"] for r in results)
            answer += f"\n\n📚 *Sources: {', '.join(sources)}*"

    # Discord has a 2000 char limit
    if len(answer) > 2000:
        answer = answer[:1997] + "..."

    await message.reply(answer)


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("ERROR: DISCORD_TOKEN not set. Copy .env.example to .env and fill it in.")
        exit(1)
    if not OPENROUTER_API_KEY:
        print("ERROR: OPENROUTER_API_KEY not set. Get one at https://openrouter.ai/keys")
        exit(1)

    client.run(DISCORD_TOKEN)
