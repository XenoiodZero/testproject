"""
Slash commands for the Discord bot.

All commands are registered via `setup_commands(tree, ctx)`.
`ctx` is a SimpleNamespace exposing: client, llm, vector_store, model, version,
authors, tools_str, start_time.

Persistent state lives in data.json next to this file:
{
  "users": {
    "<user_id>": {
      "opted_in": bool,
      "memory": [str, ...],
      "coins": int,
      "squares": {"green": int, "blue": int, "red": int},
      "food": {"<emoji>": int, ...}
    }
  },
  "servers": {
    "<guild_id>": {"context": str}
  }
}
"""

import json
import os
import random
import time
import discord
from discord import app_commands

# ---------------- Storage ----------------

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")


def _load() -> dict:
    if not os.path.exists(DATA_PATH):
        return {"users": {}, "servers": {}}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return {"users": {}, "servers": {}}
    d.setdefault("users", {})
    d.setdefault("servers", {})
    return d


def _save(data: dict) -> None:
    tmp = DATA_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, DATA_PATH)


def _user(data: dict, uid: int) -> dict:
    s = str(uid)
    if s not in data["users"]:
        data["users"][s] = {
            "opted_in": False,
            "memory": [],
            "coins": 300,
            "squares": {"green": 0, "blue": 0, "red": 0},
            "food": {},
        }
    u = data["users"][s]
    u.setdefault("opted_in", False)
    u.setdefault("memory", [])
    u.setdefault("coins", 300)
    u.setdefault("squares", {"green": 0, "blue": 0, "red": 0})
    u.setdefault("food", {})
    return u


def _server(data: dict, gid: int) -> dict:
    s = str(gid)
    if s not in data["servers"]:
        data["servers"][s] = {"context": ""}
    return data["servers"][s]


# ---------------- Permissions ----------------

def _is_admin(interaction: discord.Interaction) -> bool:
    if interaction.guild is None:
        return False
    if interaction.user.id == interaction.guild.owner_id:
        return True
    perms = interaction.user.guild_permissions
    return perms.administrator or perms.manage_guild


# ---------------- Mini-game data ----------------

SQUARE_PRICES = {"green": 20, "blue": 50, "red": 100}
SQUARE_CHANCES = {"green": 0.30, "blue": 0.60, "red": 0.90}
SQUARE_EMOJI = {"green": "🟩", "blue": "🟦", "red": "🟥"}

FOOD_EMOJIS = {
    "🍎": "apple",
    "🍌": "banana",
    "🍇": "grapes",
    "🍓": "strawberry",
    "🍑": "peach",
    "🍍": "pineapple",
    "🥝": "kiwi",
    "🍉": "watermelon",
    "🥕": "carrot",
    "🌽": "corn",
    "🍆": "eggplant",
    "🥦": "broccoli",
    "🍞": "bread",
    "🧀": "cheese",
    "🍔": "hamburger",
    "🍟": "fries",
    "🍕": "pizza",
    "🌮": "taco",
    "🌯": "burrito",
    "🍣": "sushi",
    "🍩": "doughnut",
    "🍪": "cookie",
    "🍰": "cake",
    "🍫": "chocolate",
    "🍿": "popcorn",
}


def _food_value(emoji: str) -> int:
    name = FOOD_EMOJIS.get(emoji, "")
    return max(1, len(name))


# ---------------- Helpers ----------------

def _truncate(s: str, n: int = 2000) -> str:
    return s if len(s) <= n else s[: n - 3] + "..."


# ---------------- Setup ----------------

def setup_commands(tree: app_commands.CommandTree, ctx) -> None:
    """Register all slash commands on the given CommandTree."""

    # ============ AI / Knowledge base ============

    def _answer(question: str, user_id: int, guild_id: int | None) -> str:
        data = _load()
        memory = None
        server_context = None
        if user_id is not None:
            u = data["users"].get(str(user_id))
            if u and u.get("opted_in"):
                memory = u.get("memory") or None
        if guild_id is not None:
            sv = data["servers"].get(str(guild_id))
            if sv and sv.get("context"):
                server_context = sv["context"]

        results = ctx.vector_store.query(question, top_k=3)
        answer = ctx.llm.generate(question, results, user_memory=memory, server_context=server_context)
        if results:
            sources = set(r["source"] for r in results)
            answer += f"\n\n📚 *Sources: {', '.join(sources)}*"
        return _truncate(answer)

    @tree.command(name="ask", description="Ask a question against the knowledge base")
    @app_commands.describe(question="Your question")
    async def ask_slash(interaction: discord.Interaction, question: str):
        await interaction.response.defer(thinking=True)
        answer = _answer(
            question,
            interaction.user.id,
            interaction.guild.id if interaction.guild else None,
        )
        await interaction.followup.send(answer)

    def _classify_attachment(att: discord.Attachment) -> str | None:
        c = (att.content_type or "").lower()
        n = att.filename.lower()
        if c.startswith("image/") or n.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            return "image"
        if c.startswith("text/") or n.endswith(
            (".txt", ".md", ".log", ".csv", ".json", ".py", ".js", ".ts", ".yml", ".yaml")
        ):
            return "text"
        return None

    @tree.command(name="ask_file", description="Ask a question with an attached text file or image")
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
        await interaction.response.defer(thinking=True)
        payload, skipped = [], []
        MAX = 5 * 1024 * 1024
        for att in [a for a in (file1, file2, file3) if a is not None]:
            kind = _classify_attachment(att)
            if kind is None:
                skipped.append(f"{att.filename} (unsupported)")
                continue
            if att.size > MAX:
                skipped.append(f"{att.filename} (too large)")
                continue
            try:
                data_bytes = await att.read()
            except Exception as e:
                skipped.append(f"{att.filename} ({e})")
                continue
            payload.append({
                "kind": kind,
                "media_type": att.content_type or ("image/png" if kind == "image" else "text/plain"),
                "data": data_bytes,
                "filename": att.filename,
            })

        data = _load()
        memory = None
        server_context = None
        u = data["users"].get(str(interaction.user.id))
        if u and u.get("opted_in"):
            memory = u.get("memory") or None
        if interaction.guild:
            sv = data["servers"].get(str(interaction.guild.id))
            if sv and sv.get("context"):
                server_context = sv["context"]

        results = ctx.vector_store.query(question, top_k=3)
        answer = ctx.llm.generate_with_attachments(
            question, results, payload, user_memory=memory, server_context=server_context
        )
        if results:
            sources = set(r["source"] for r in results)
            answer += f"\n\n📚 *Sources: {', '.join(sources)}*"
        if skipped:
            answer += f"\n\n⚠️ *Skipped: {', '.join(skipped)}*"
        await interaction.followup.send(_truncate(answer))

    # ============ Status / Credits ============

    @tree.command(name="status", description="Show bot status")
    async def status_slash(interaction: discord.Interaction):
        uptime = int(time.time() - ctx.start_time)
        h, rem = divmod(uptime, 3600)
        m, s = divmod(rem, 60)
        embed = discord.Embed(title="Bot Status", color=0x00B894)
        embed.add_field(name="Status", value="🟢 Online", inline=True)
        embed.add_field(name="Uptime", value=f"{h}h {m}m {s}s", inline=True)
        embed.add_field(name="Latency", value=f"{round(ctx.client.latency * 1000)} ms", inline=True)
        embed.add_field(name="Provider", value="Anthropic Claude", inline=True)
        embed.add_field(name="Model", value=ctx.model, inline=True)
        embed.add_field(name="Guilds", value=str(len(ctx.client.guilds)), inline=True)
        embed.add_field(name="Knowledge base", value=f"{ctx.vector_store.index.ntotal} chunks", inline=True)
        embed.add_field(name="Version", value=ctx.version, inline=True)
        await interaction.response.send_message(embed=embed)

    @tree.command(name="credits", description="Show bot credits and tools used")
    async def credits_slash(interaction: discord.Interaction):
        embed = discord.Embed(
            title="Bot Credits",
            description="A RAG-powered Discord bot with Claude vision/file support and a mini-game.",
            color=0x6C5CE7,
        )
        embed.add_field(name="Author(s)", value=ctx.authors, inline=False)
        embed.add_field(name="Version", value=ctx.version, inline=True)
        embed.add_field(name="LLM", value=f"Anthropic Claude ({ctx.model})", inline=True)
        embed.add_field(name="Tools & libraries", value=ctx.tools_str, inline=False)
        await interaction.response.send_message(embed=embed)

    # ============ Privacy ============

    @tree.command(name="privacy_optin", description="Opt in to having the bot remember context about you")
    async def privacy_optin(interaction: discord.Interaction):
        data = _load()
        u = _user(data, interaction.user.id)
        u["opted_in"] = True
        _save(data)
        await interaction.response.send_message(
            "✅ You have opted in. The bot may now remember facts you tell it via `/remember`.",
            ephemeral=True,
        )

    @tree.command(name="privacy_optout", description="Opt out of bot memory (does not delete existing data)")
    async def privacy_optout(interaction: discord.Interaction):
        data = _load()
        u = _user(data, interaction.user.id)
        u["opted_in"] = False
        _save(data)
        await interaction.response.send_message(
            "🚫 You have opted out. Use `/forget_me` to also delete stored data.",
            ephemeral=True,
        )

    @tree.command(name="privacy_status", description="Show your privacy status and stored memory")
    async def privacy_status(interaction: discord.Interaction):
        data = _load()
        u = data["users"].get(str(interaction.user.id))
        if not u:
            await interaction.response.send_message("No data stored for you.", ephemeral=True)
            return
        mem = "\n".join(f"- {m}" for m in u.get("memory", [])) or "_(empty)_"
        await interaction.response.send_message(
            f"**Opted in:** {u.get('opted_in', False)}\n**Memory:**\n{mem}",
            ephemeral=True,
        )

    @tree.command(name="remember", description="Save a fact about yourself (requires opt-in)")
    @app_commands.describe(fact="Something for the bot to remember about you")
    async def remember_cmd(interaction: discord.Interaction, fact: str):
        data = _load()
        u = _user(data, interaction.user.id)
        if not u["opted_in"]:
            await interaction.response.send_message(
                "You must `/privacy_optin` first.", ephemeral=True
            )
            return
        u["memory"].append(fact)
        _save(data)
        await interaction.response.send_message("📝 Saved.", ephemeral=True)

    @tree.command(name="forget_me", description="Delete all stored data about you")
    async def forget_me(interaction: discord.Interaction):
        data = _load()
        if str(interaction.user.id) in data["users"]:
            del data["users"][str(interaction.user.id)]
            _save(data)
        await interaction.response.send_message("🗑️ All your data has been deleted.", ephemeral=True)

    # ============ Admin ============

    @tree.command(name="admin_view_user", description="(Admin) View a user's stored data")
    @app_commands.describe(user="The user to inspect")
    async def admin_view_user(interaction: discord.Interaction, user: discord.User):
        if not _is_admin(interaction):
            await interaction.response.send_message("⛔ You need Manage Server.", ephemeral=True)
            return
        data = _load()
        u = data["users"].get(str(user.id))
        if not u:
            await interaction.response.send_message("No data for that user.", ephemeral=True)
            return
        await interaction.response.send_message(
            f"```json\n{_truncate(json.dumps(u, indent=2), 1900)}\n```", ephemeral=True
        )

    @tree.command(name="admin_edit_user_memory", description="(Admin) Replace a user's memory list")
    @app_commands.describe(user="User", memory="Newline-separated memory entries")
    async def admin_edit_user_memory(
        interaction: discord.Interaction, user: discord.User, memory: str
    ):
        if not _is_admin(interaction):
            await interaction.response.send_message("⛔ You need Manage Server.", ephemeral=True)
            return
        data = _load()
        u = _user(data, user.id)
        u["memory"] = [line.strip() for line in memory.splitlines() if line.strip()]
        _save(data)
        await interaction.response.send_message("✅ Updated.", ephemeral=True)

    @tree.command(name="admin_delete_user", description="(Admin) Delete all data for a user")
    @app_commands.describe(user="User to delete")
    async def admin_delete_user(interaction: discord.Interaction, user: discord.User):
        if not _is_admin(interaction):
            await interaction.response.send_message("⛔ You need Manage Server.", ephemeral=True)
            return
        data = _load()
        if str(user.id) in data["users"]:
            del data["users"][str(user.id)]
            _save(data)
        await interaction.response.send_message(f"🗑️ Deleted data for {user.mention}.", ephemeral=True)

    @tree.command(name="admin_view_server", description="(Admin) View the server's stored context")
    async def admin_view_server(interaction: discord.Interaction):
        if not _is_admin(interaction):
            await interaction.response.send_message("⛔ You need Manage Server.", ephemeral=True)
            return
        data = _load()
        sv = data["servers"].get(str(interaction.guild.id), {"context": ""})
        text = sv.get("context", "") or "_(empty)_"
        await interaction.response.send_message(f"**Server context:**\n```\n{_truncate(text, 1900)}\n```", ephemeral=True)

    @tree.command(name="admin_edit_server", description="(Admin) Set the server's context")
    @app_commands.describe(context="New server context")
    async def admin_edit_server(interaction: discord.Interaction, context: str):
        if not _is_admin(interaction):
            await interaction.response.send_message("⛔ You need Manage Server.", ephemeral=True)
            return
        data = _load()
        sv = _server(data, interaction.guild.id)
        sv["context"] = context
        _save(data)
        await interaction.response.send_message("✅ Server context updated.", ephemeral=True)

    @tree.command(name="admin_delete_server", description="(Admin) Delete this server's context")
    async def admin_delete_server(interaction: discord.Interaction):
        if not _is_admin(interaction):
            await interaction.response.send_message("⛔ You need Manage Server.", ephemeral=True)
            return
        data = _load()
        if str(interaction.guild.id) in data["servers"]:
            del data["servers"][str(interaction.guild.id)]
            _save(data)
        await interaction.response.send_message("🗑️ Server context deleted.", ephemeral=True)

    # ============ Mini-game ============

    @tree.command(name="game_start", description="Initialize your mini-game profile (300 starter coins)")
    async def game_start(interaction: discord.Interaction):
        data = _load()
        existed = str(interaction.user.id) in data["users"]
        u = _user(data, interaction.user.id)
        _save(data)
        msg = "Welcome back!" if existed else "🎉 Profile created with 300 coins!"
        await interaction.response.send_message(
            f"{msg}\nUse `/shop`, `/buy`, `/capture`, `/inventory`, `/sell`.",
            ephemeral=True,
        )

    @tree.command(name="shop", description="Show the square shop")
    async def shop(interaction: discord.Interaction):
        embed = discord.Embed(title="🛒 Square Shop", color=0xFDCB6E)
        for color, price in SQUARE_PRICES.items():
            chance = int(SQUARE_CHANCES[color] * 100)
            embed.add_field(
                name=f"{SQUARE_EMOJI[color]} {color.title()} square",
                value=f"Price: **{price}** coins\nCapture chance: **{chance}%**",
                inline=True,
            )
        embed.set_footer(text="Buy with /buy color amount")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="buy", description="Buy squares from the shop")
    @app_commands.describe(color="green | blue | red", amount="How many to buy")
    @app_commands.choices(color=[
        app_commands.Choice(name="green", value="green"),
        app_commands.Choice(name="blue", value="blue"),
        app_commands.Choice(name="red", value="red"),
    ])
    async def buy(interaction: discord.Interaction, color: app_commands.Choice[str], amount: int):
        if amount <= 0:
            await interaction.response.send_message("Amount must be positive.", ephemeral=True)
            return
        data = _load()
        u = _user(data, interaction.user.id)
        cost = SQUARE_PRICES[color.value] * amount
        if u["coins"] < cost:
            await interaction.response.send_message(
                f"Not enough coins. Need {cost}, have {u['coins']}.", ephemeral=True
            )
            return
        u["coins"] -= cost
        u["squares"][color.value] += amount
        _save(data)
        await interaction.response.send_message(
            f"Bought {amount}× {SQUARE_EMOJI[color.value]} for {cost} coins. "
            f"Coins left: {u['coins']}.",
            ephemeral=True,
        )

    @tree.command(name="capture", description="Use a square to attempt capturing a random food")
    @app_commands.describe(color="Which square to use")
    @app_commands.choices(color=[
        app_commands.Choice(name="green", value="green"),
        app_commands.Choice(name="blue", value="blue"),
        app_commands.Choice(name="red", value="red"),
    ])
    async def capture(interaction: discord.Interaction, color: app_commands.Choice[str]):
        data = _load()
        u = _user(data, interaction.user.id)
        c = color.value
        if u["squares"][c] <= 0:
            await interaction.response.send_message(
                f"You have no {SQUARE_EMOJI[c]} squares. Buy some with `/buy`.",
                ephemeral=True,
            )
            return
        u["squares"][c] -= 1
        food = random.choice(list(FOOD_EMOJIS.keys()))
        chance = SQUARE_CHANCES[c]
        if random.random() < chance:
            u["food"][food] = u["food"].get(food, 0) + 1
            _save(data)
            await interaction.response.send_message(
                f"{SQUARE_EMOJI[c]} → wild {food} ({FOOD_EMOJIS[food]}) appeared… **caught!** 🎉"
            )
        else:
            _save(data)
            await interaction.response.send_message(
                f"{SQUARE_EMOJI[c]} → wild {food} ({FOOD_EMOJIS[food]}) appeared… **escaped!** 💨"
            )

    @tree.command(name="inventory", description="Show your inventory")
    async def inventory(interaction: discord.Interaction):
        data = _load()
        u = _user(data, interaction.user.id)
        squares = " ".join(f"{SQUARE_EMOJI[c]}×{u['squares'][c]}" for c in ("green", "blue", "red"))
        if u["food"]:
            food_lines = "\n".join(
                f"{e}×{n} _(sells {_food_value(e) * n})_"
                for e, n in sorted(u["food"].items(), key=lambda x: -x[1])
            )
        else:
            food_lines = "_(none)_"
        embed = discord.Embed(title=f"🎒 {interaction.user.display_name}'s inventory", color=0x55EFC4)
        embed.add_field(name="💰 Coins", value=str(u["coins"]), inline=False)
        embed.add_field(name="Squares", value=squares, inline=False)
        embed.add_field(name="Food", value=food_lines, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tree.command(name="sell", description="Sell a food emoji from your inventory")
    @app_commands.describe(food="The food emoji to sell", amount="How many (default 1)")
    async def sell(interaction: discord.Interaction, food: str, amount: int = 1):
        if food not in FOOD_EMOJIS:
            await interaction.response.send_message(
                "That isn't a known food emoji. Try one shown in `/inventory`.",
                ephemeral=True,
            )
            return
        if amount <= 0:
            await interaction.response.send_message("Amount must be positive.", ephemeral=True)
            return
        data = _load()
        u = _user(data, interaction.user.id)
        have = u["food"].get(food, 0)
        if have < amount:
            await interaction.response.send_message(
                f"You only have {have}× {food}.", ephemeral=True
            )
            return
        value = _food_value(food) * amount
        u["food"][food] = have - amount
        if u["food"][food] == 0:
            del u["food"][food]
        u["coins"] += value
        _save(data)
        await interaction.response.send_message(
            f"Sold {amount}× {food} for **{value}** coins. Total: {u['coins']}.",
            ephemeral=True,
        )

    @tree.command(name="sell_all", description="Sell every food emoji in your inventory")
    async def sell_all(interaction: discord.Interaction):
        data = _load()
        u = _user(data, interaction.user.id)
        if not u["food"]:
            await interaction.response.send_message("Nothing to sell.", ephemeral=True)
            return
        total = sum(_food_value(e) * n for e, n in u["food"].items())
        u["food"] = {}
        u["coins"] += total
        _save(data)
        await interaction.response.send_message(
            f"💰 Sold everything for **{total}** coins. Total: {u['coins']}.",
            ephemeral=True,
        )
