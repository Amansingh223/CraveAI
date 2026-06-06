# CraveAI — Your Personal AI Chef

Hey there! Welcome to CraveAI. 

I built this project to solve that daily problem of staring at the fridge and thinking: *"What do I cook with this?"* It's a full-stack AI recipe generator that takes whatever ingredients you have, asks for your preferences (like time, cuisine, and diet), and spits out custom recipes complete with real food photos. 

I recently migrated the architecture to a split backend (FastAPI) and frontend (Streamlit) for better scalability, and hooked it up to Llama 3 via Groq for insanely fast responses.

---

##  Live Demos

Yep, it's live! You can play around with it here:

- **Frontend (Streamlit):** [https://craveai-foodstream.streamlit.app/](https://craveai-foodstream.streamlit.app/)
- **Backend API (FastAPI):** [https://craveai-br26.onrender.com/docs](https://craveai-br26.onrender.com/docs) *(Check out the Swagger UI if you want to hit the endpoints directly!)*

---

##  How It Works (The Tech Stack)

- **UI:** Streamlit (because it's fast and looks great)
- **Backend:** FastAPI (handling all the heavy lifting)
- **AI Brain:** Llama 3 (running on the Groq API for near-instant inference)
- **Images:** Unsplash API (for fetching high-quality food photography)
- **Orchestration:** LangChain

---

##  Running It Locally

Want to run it on your own machine? It's pretty straightforward.

**1. Clone this repo & install the dependencies:**
```bash
git clone https://github.com/Amansingh223/CraveAI.git
cd CraveAI
pip install -r requirements.txt
```

**2. Setup your API keys:**
Create a `.env` file in the root folder and drop your keys in there:
```env
GROQ_API_KEY=your_groq_api_key_here
UNSPLASH_ACCESS_KEY=your_unsplash_key_here
```
**3. Fire it up:**
If you're on Windows, just double click the `run.bat` file! It will automatically boot up both the FastAPI backend and the Streamlit frontend. 

If you prefer doing it manually:
- Open Terminal 1: `uvicorn src.api.main:app --reload --port 8000`
- Open Terminal 2: `streamlit run app/main.py`

---

##  Project Structure

Here's how I organized the code (trying to keep it clean and modular):

```text
CraveAI/
├── app/                    # The Streamlit frontend code
│   └── main.py             
├── src/                    # The Backend logic
│   ├── api/                
│   │   └── main.py         # FastAPI endpoints and Pydantic models
│   ├── llm/
│   │   └── engine.py       # Prompt engineering & LangChain setup
│   └── utils/
│       └── images.py       # Code that talks to Unsplash
├── data/                   # Where the user feedback gets saved (feedback.json)
├── notebooks/              # Scratchpad for data experiments
├── run.bat                 # Handy script to launch everything locally
└── requirements.txt        
```

---
*Feel free to fork this, submit PRs, or just use it to figure out what to make for dinner tonight!* 
