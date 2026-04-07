"""
RAG AI Discord Bot
Main entrypoint — loads knowledge base, connects to Discord, handles messages.
"""

import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from vector_store import VectorStore
from llm_client import LLMClient, ClaudeClient

load_dotenv()

# --- Config ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/llama-3-8b-instruct:free")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-6")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
# Provider: "claude" or "openrouter". Defaults to claude if a key is set.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "claude" if ANTHROPIC_API_KEY else "openrouter").lower()
BOT_PREFIX = "!ask"

# --- Init components ---
print("[Bot] Loading vector store...")
vector_store = VectorStore(embedding_model=EMBEDDING_MODEL)
vector_store.load_documents("knowledge_base")
vector_store.build_index()

print(f"[Bot] Initializing LLM client (provider={LLM_PROVIDER})...")
if LLM_PROVIDER == "claude":
    llm = ClaudeClient(api_key=ANTHROPIC_API_KEY, model=CLAUDE_MODEL)
    ACTIVE_MODEL = CLAUDE_MODEL
else:
    llm = LLMClient(api_key=OPENROUTER_API_KEY, model=LLM_MODEL)
    ACTIVE_MODEL = LLM_MODEL

# --- Discord bot ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def _answer(question: str) -> str:
    results = vector_store.query(question, top_k=3)
    answer = llm.generate(question, results)
    if results:
        sources = set(r["source"] for r in results)
        answer += f"\n\n📚 *Sources: {', '.join(sources)}*"
    if len(answer) > 2000:
        answer = answer[:1997] + "..."
    return answer


@client.event
async def on_ready():
    print(f"[Bot] Logged in as {client.user}")
    print(f"[Bot] Knowledge base: {vector_store.index.ntotal} indexed chunks")
    print(f"[Bot] Using model: {ACTIVE_MODEL}")
    try:
        synced = await tree.sync()
        print(f"[Bot] Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"[Bot] Failed to sync slash commands: {e}")


@tree.command(name="ask", description="Ask a question against the knowledge base")
@app_commands.describe(question="Your question")
async def ask_slash(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=True)
    answer = _answer(question)
    await interaction.followup.send(answer)


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if not message.content.startswith(BOT_PREFIX):
        return

    question = message.content[len(BOT_PREFIX):].strip()
    if not question:
        await message.reply("Please ask a question! Example: `!ask What is RAG?`")
        return

    async with message.channel.typing():
        answer = _answer(question)

    await message.reply(answer)


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("ERROR: DISCORD_TOKEN not set. Copy .env.example to .env and fill it in.")
        exit(1)
    if LLM_PROVIDER == "claude" and not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set. Get one at https://console.anthropic.com/")
        exit(1)
    if LLM_PROVIDER == "openrouter" and not OPENROUTER_API_KEY:
        print("ERROR: OPENROUTER_API_KEY not set. Get one at https://openrouter.ai/keys")
        exit(1)

    client.run(DISCORD_TOKEN)
