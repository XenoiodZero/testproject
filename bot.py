"""
RAG AI Discord Bot
Main entrypoint — loads knowledge base, connects to Discord, handles messages.
"""

import os
import time
import discord
from discord import app_commands
from dotenv import load_dotenv
from vector_store import VectorStore
from llm_client import LLMClient, ClaudeClient

START_TIME = time.time()
BOT_VERSION = "0.2.0"
BOT_AUTHORS = "XenoiodZero"
BOT_TOOLS = (
    "Python, discord.py, FAISS, sentence-transformers, "
    "Anthropic Claude API, OpenRouter (OpenAI SDK), python-dotenv"
)

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


@tree.command(name="status", description="Show bot status")
async def status_slash(interaction: discord.Interaction):
    uptime = int(time.time() - START_TIME)
    h, rem = divmod(uptime, 3600)
    m, s = divmod(rem, 60)
    embed = discord.Embed(title="Bot Status", color=0x00b894)
    embed.add_field(name="Status", value="🟢 Online", inline=True)
    embed.add_field(name="Uptime", value=f"{h}h {m}m {s}s", inline=True)
    embed.add_field(name="Latency", value=f"{round(client.latency * 1000)} ms", inline=True)
    embed.add_field(name="Provider", value=LLM_PROVIDER, inline=True)
    embed.add_field(name="Model", value=ACTIVE_MODEL, inline=True)
    embed.add_field(name="Guilds", value=str(len(client.guilds)), inline=True)
    embed.add_field(
        name="Knowledge base",
        value=f"{vector_store.index.ntotal} chunks",
        inline=True,
    )
    embed.add_field(name="Version", value=BOT_VERSION, inline=True)
    await interaction.response.send_message(embed=embed)


@tree.command(name="credits", description="Show bot credits and tools used")
async def credits_slash(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Bot Credits",
        description="A RAG-powered Discord bot with Claude vision/file support.",
        color=0x6c5ce7,
    )
    embed.add_field(name="Author(s)", value=BOT_AUTHORS, inline=False)
    embed.add_field(name="Version", value=BOT_VERSION, inline=True)
    embed.add_field(name="LLM", value=f"{LLM_PROVIDER} ({ACTIVE_MODEL})", inline=True)
    embed.add_field(name="Tools & libraries", value=BOT_TOOLS, inline=False)
    embed.add_field(
        name="Built with",
        value="Anthropic Claude API · discord.py · FAISS · sentence-transformers",
        inline=False,
    )
    await interaction.response.send_message(embed=embed)


def _classify_attachment(att: discord.Attachment) -> str | None:
    ct = (att.content_type or "").lower()
    name = att.filename.lower()
    if ct.startswith("image/") or name.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
        return "image"
    if ct.startswith("text/") or name.endswith(
        (".txt", ".md", ".log", ".csv", ".json", ".py", ".js", ".ts", ".yml", ".yaml")
    ):
        return "text"
    return None


@tree.command(
    name="ask_file",
    description="Ask a question with an attached text file or image",
)
@app_commands.describe(
    question="Your question",
    file1="A text file or image",
    file2="(optional) second attachment",
    file3="(optional) third attachment",
)
async def ask_file_slash(
    interaction: discord.Interaction,
    question: str,
    file1: discord.Attachment,
    file2: discord.Attachment | None = None,
    file3: discord.Attachment | None = None,
):
    if not isinstance(llm, ClaudeClient):
        await interaction.response.send_message(
            "File/image attachments are only supported with the Claude provider. "
            "Set `LLM_PROVIDER=claude` and `ANTHROPIC_API_KEY`.",
            ephemeral=True,
        )
        return

    await interaction.response.defer(thinking=True)

    attachments_payload = []
    skipped = []
    MAX_BYTES = 5 * 1024 * 1024  # 5 MB per file

    for att in [a for a in (file1, file2, file3) if a is not None]:
        kind = _classify_attachment(att)
        if kind is None:
            skipped.append(f"{att.filename} (unsupported type)")
            continue
        if att.size > MAX_BYTES:
            skipped.append(f"{att.filename} (too large)")
            continue
        try:
            data = await att.read()
        except Exception as e:
            skipped.append(f"{att.filename} ({e})")
            continue
        attachments_payload.append(
            {
                "kind": kind,
                "media_type": att.content_type or ("image/png" if kind == "image" else "text/plain"),
                "data": data,
                "filename": att.filename,
            }
        )

    results = vector_store.query(question, top_k=3)
    answer = llm.generate_with_attachments(question, results, attachments_payload)

    if results:
        sources = set(r["source"] for r in results)
        answer += f"\n\n📚 *Sources: {', '.join(sources)}*"
    if skipped:
        answer += f"\n\n⚠️ *Skipped: {', '.join(skipped)}*"
    if len(answer) > 2000:
        answer = answer[:1997] + "..."

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
