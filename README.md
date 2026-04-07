# RAG AI Discord Bot

A Discord bot that uses Retrieval-Augmented Generation (RAG) to answer questions from a curated knowledge base. Instead of relying solely on a language model's training data, the bot retrieves relevant documents before generating a response — reducing hallucinations and grounding answers in real sources.

## How It Works

```
User Question → Embedding → FAISS Vector Search → Retrieved Context → LLM Generation → Discord Response
```

1. User sends `!ask <question>` in Discord
2. The question is embedded using `sentence-transformers` (all-MiniLM-L6-v2)
3. FAISS searches the vector index for the most relevant document chunks
4. Retrieved chunks are injected into the LLM prompt as context
5. The LLM (via OpenRouter) generates a grounded response
6. The bot replies in Discord with the answer and sources

## Project Structure

```
RAGAIDiscordBot/
├── bot.py              # Main entrypoint — Discord bot logic
├── vector_store.py     # Document loading, chunking, embedding, FAISS indexing & retrieval
├── llm_client.py       # OpenRouter API client with RAG prompt construction
├── knowledge_base/     # Drop .txt or .md files here — they become searchable context
│   └── rag_overview.txt
├── requirements.txt
├── .env.example        # Template for API keys
└── .gitignore
```

## Setup

### Prerequisites
- Python 3.10+
- A Discord bot token ([create one here](https://discord.com/developers/applications))
- An OpenRouter API key ([get one here](https://openrouter.ai/keys))

### Installation

```bash
git clone https://github.com/Nightmare0409/RAGAIDiscordBot.git
cd RAGAIDiscordBot
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your tokens
```

### Running

```bash
python bot.py
```

The bot will load all `.txt` and `.md` files from `knowledge_base/`, build the vector index, and connect to Discord.

### Adding Knowledge

Drop any `.txt` or `.md` files into the `knowledge_base/` folder and restart the bot. They will be automatically chunked, embedded, and indexed.

## Technologies

| Component | Technology |
|---|---|
| Bot framework | discord.py |
| LLM API | OpenRouter (OpenAI-compatible) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector search | FAISS (faiss-cpu) |
| Language | Python 3.10+ |

## Citations & Acknowledgements

- [discord.py](https://github.com/Rapptz/discord.py)
- [OpenRouter](https://openrouter.ai/)
- [FAISS](https://github.com/facebookresearch/faiss) — Meta AI
- [Sentence-Transformers](https://www.sbert.net/) — UKP Lab
- [OpenAI Python SDK](https://github.com/openai/openai-python) (used for OpenRouter compatibility)
