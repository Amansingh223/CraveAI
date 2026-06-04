# 🍳 CraveAI — AI Recipe Generator

> An intelligent recipe generation app powered by **Llama 3 (Groq)** and **Langchain**, with real food photography from **Unsplash**.

---

## 🗂️ Project Structure

```text
CraveAI/
├── app/                    # Streamlit UI Layer
│   └── main.py             # Main Streamlit application entry point
│
├── src/                    # Core AI/ML Logic
│   ├── llm/
│   │   └── engine.py       # Prompt engineering + Groq/Langchain LLM pipeline
│   └── utils/
│       └── images.py       # Unsplash API integration for food images
│
├── notebooks/              # Experimentation & analysis (Jupyter Notebooks)
│
├── data/                   # Static datasets / offline recipe JSON cache
│
├── .env                    # Environment variables (local only, not committed)
├── requirements.txt        # Python dependencies
├── Procfile                # Deployment config for cloud platforms
└── README.md
```

## ⚡ Tech Stack

| Layer | Technology |
|---|---|
| **UI** | Streamlit |
| **LLM** | Llama 3 via Groq API |
| **Orchestration** | Langchain |
| **Image API** | Unsplash |
| **Env Management** | python-dotenv |

## 🚀 Local Setup

**1. Clone and install dependencies:**
```bash
git clone https://github.com/your-username/crave-ai.git
cd crave-ai
pip install -r requirements.txt
```

**2. Create `.env` file with your keys:**
```env
GROQ_API_KEY=your_groq_api_key_here
UNSPLASH_ACCESS_KEY=your_unsplash_key_here
```

**3. Run the app:**
```bash
streamlit run app/main.py
```

## ☁️ Streamlit Cloud Deployment

1. Push the repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and connect your repo.
3. Set **Main file path** to `app/main.py`.
4. Add `GROQ_API_KEY` and `UNSPLASH_ACCESS_KEY` under **Secrets**.
5. Deploy! 🎉

## 🔑 Getting API Keys

- **Groq API (Free):** [console.groq.com](https://console.groq.com/)
- **Unsplash API (Free):** [unsplash.com/developers](https://unsplash.com/developers)
