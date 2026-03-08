😫 The Problem
Traditional Research Workflow (Painful):
─────────────────────────────────────────
📄 Open paper 1... read 20 pages
📄 Open paper 2... read 18 pages
📄 Open paper 3... read 25 pages
🤔 Try to remember what paper 1 said about X...
😩 Can't find the exact part...
🔁 Repeat for 47 more papers...
⏰ Hours wasted. Notes scattered. Brain exhausted.
😊 Our Solution
ResearchHub AI Workflow (Easy):
────────────────────────────────────────────────
🔍 Search "transformer attention mechanism"
📥 Click Import on the top 5 results
💬 Ask: "How does attention work across these papers?"
🤖 AI reads all 5 papers and gives you a clear answer
💡 Ask: "What are the key differences between them?"
🤖 AI compares them in a structured table
⏰ Done in 10 minutes. Accurate. Cited. ✅
🎯 Who is this for?
<table>
<tr>
<td align="center" width="25%">
🎓
Students
Writing a thesis or literature review
</td>
<td align="center" width="25%">
🔬
Researchers
Keeping up with new papers in your field
</td>
<td align="center" width="25%">
👨‍💻
Developers
Learning about ML/AI techniques
</td>
<td align="center" width="25%">
🏢
Professionals
Research-based decision making
</td>
</tr>
</table>
<br/>

🏗️ How It All Works

Totally new to programming? Think of it like a restaurant.
The Frontend is the menu you see. The Backend is the kitchen.
Axios is the waiter carrying your order. SQLite is the pantry storing ingredients.

<br/>
```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           ResearchHub AI — System Map                        │
│                                                                              │
│   ┌────────────────────────────────────┐                                     │
│   │   🌐  BROWSER (localhost:3000)      │                                     │
│   │                                    │                                     │
│   │   ┌──────────┐  ┌───────────────┐  │                                     │
│   │   │  Login   │  │   Workspace   │  │                                     │
│   │   │  Page    │  │   Sidebar     │  │                                     │
│   │   └──────────┘  └───────────────┘  │                                     │
│   │   ┌──────────┐  ┌───────────────┐  │                                     │
│   │   │  Search  │  │   AI Chat     │  │                                     │
│   │   │  Papers  │  │   Interface   │  │                                     │
│   │   └──────────┘  └───────────────┘  │                                     │
│   │           Built with React ⚛️       │                                     │
│   └──────────────┬─────────────────────┘                                     │
│                  │                                                            │
│          Axios sends requests                                                 │
│          with JWT token 🔐                                                    │
│                  │                                                            │
│   ┌──────────────▼─────────────────────┐                                     │
│   │   ⚙️  BACKEND (localhost:8000)      │                                     │
│   │                                    │                                     │
│   │   /auth/*    → Login & Register    │                                     │
│   │   /papers/*  → Search & Import ────────→ 🌐 arXiv API (2M+ papers)      │
│   │   /chat/*    → AI Conversations   │                                      │
│   │       │                           │                                      │
│   │       ▼                           │                                      │
│   │   🧠 AI Utils                     │                                      │
│   │   ├─ vector_db.py                 │                                      │
│   │   │   Converts text → numbers     │                                      │
│   │   │   Finds similar papers        │                                      │
│   │   ├─ groq_client.py               │                                      │
│   │   │   Calls Llama 3.3 70B ─────────────→ 🤖 Groq API                   │
│   │   └─ research_assistant.py        │                                      │
│   │       Orchestrates all AI tasks   │                                      │
│   │               │                   │                                      │
│   │               ▼                   │                                      │
│   │         🗄️ SQLite DB              │                                      │
│   │   Users│Workspaces│Papers│Chats   │                                      │
│   └────────────────────────────────────┘                                     │
└──────────────────────────────────────────────────────────────────────────────┘
```
<br/>
🔄 What happens when you send a chat message?
You type: "What is the main contribution of these papers?"
    │
    ▼ (1) Frontend sends message to POST /chat/
    │
    ▼ (2) Backend receives it
    │
    ▼ (3) vector_db.py converts your question to 384 numbers (a "vector")
    │
    ▼ (4) Compares your vector to all paper abstracts
    │     → Finds top 3 most relevant papers
    │
    ▼ (5) Builds a prompt: "Here are 3 papers: [abstracts]. Answer: what is their contribution?"
    │
    ▼ (6) Sends to Groq → Llama 3.3 70B processes it (~500 tokens/sec)
    │
    ▼ (7) AI response comes back
    │
    ▼ (8) Saved to SQLite database (chat history)
    │
    ▼ (9) Returned to frontend → displayed in chat bubble
    
You see the answer in ~2 seconds ✅
<br/>

🛠️ Tech Stack — Explained Simply
<br/>

Every technology choice is explained like you've never heard of it before.

<br/>
<table>
<thead>
<tr>
<th>🏷️ Layer</th>
<th>Technology</th>
<th>🤔 What is it?</th>
<th>💡 Why we use it</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>🖥️ UI</b></td>
<td>
React 18
</td>
<td>A JavaScript library that builds interactive websites. Instead of reloading the whole page, only the changed parts update.</td>
<td>Fast, component-based, huge community</td>
</tr>
<tr>
<td><b>📝 Types</b></td>
<td>
TypeScript
</td>
<td>JavaScript with type safety. Like writing code with spell-check — catches bugs before they happen.</td>
<td>Fewer bugs, better autocomplete in VS Code</td>
</tr>
<tr>
<td><b>🎨 Style</b></td>
<td>
Tailwind CSS
</td>
<td>CSS framework where you style using class names like `bg-blue-500`. No separate CSS files needed.</td>
<td>Fast to write, consistent design</td>
</tr>
<tr>
<td><b>📡 HTTP</b></td>
<td>
Axios
</td>
<td>JavaScript library for making HTTP requests. Like `fetch()` but smarter — handles errors, headers, tokens automatically.</td>
<td>Auto-attaches JWT token to every request</td>
</tr>
<tr>
<td><b>⚙️ Backend</b></td>
<td>
FastAPI
</td>
<td>Python web framework for building APIs. Automatically creates documentation and validates data types.</td>
<td>Fast, auto-docs at /docs, Python-native</td>
</tr>
<tr>
<td><b>🗄️ Database</b></td>
<td>
SQLite + SQLAlchemy
</td>
<td>SQLite is a database stored in one file. SQLAlchemy lets you write Python classes instead of SQL queries.</td>
<td>No setup needed, perfect for local dev</td>
</tr>
<tr>
<td><b>🔐 Security</b></td>
<td>
JWT + bcrypt
</td>
<td>JWT = a digital ID card that proves you're logged in. bcrypt = scrambles passwords so even we can't read them.</td>
<td>Industry standard authentication</td>
</tr>
<tr>
<td><b>🤖 AI Model</b></td>
<td>
Llama 3.3 70B
</td>
<td>Open-source large language model by Meta with 70 billion parameters. Runs on Groq's custom chips for ultra-fast inference.</td>
<td>Free, fast (~500 tok/s), very capable</td>
</tr>
<tr>
<td><b>🧬 Embeddings</b></td>
<td>
sentence-transformers
</td>
<td>Converts sentences to lists of numbers (vectors) that capture meaning. Similar sentences get similar numbers.</td>
<td>Enables semantic search across papers</td>
</tr>
<tr>
<td><b>📚 Papers</b></td>
<td>
arXiv API
</td>
<td>Free XML API from Cornell University that gives access to 2M+ academic preprints. No key needed.</td>
<td>Free, reliable, massive paper database</td>
</tr>
</tbody>
</table>
<br/>

📁 Project Structure — Every File Explained
<br/>
```
🗂️ ResearchHubAI/
│
├── 🔑 .env                          SECRET KEYS — never share or commit this!
├── 🚫 .gitignore                    Tells Git to ignore .env, node_modules, etc.
├── 📋 requirements.txt              Python packages list (like package.json for Python)
├── 📖 README.md                     This file!
│
├── 🐍 backend/                      Everything running on the SERVER side
│   │
│   ├── 🚪 main.py                   Entry point — creates FastAPI app, adds CORS,
│   │                                calls create_tables() on startup
│   │
│   ├── 📂 models/
│   │   └── 🗄️ database.py           Database schema — defines 4 tables:
│   │                                ┌──────────┬──────────────────────────────┐
│   │                                │ Table    │ Columns                      │
│   │                                ├──────────┼──────────────────────────────┤
│   │                                │ User     │ id, username, email, password │
│   │                                │ Workspace│ id, name, owner_id           │
│   │                                │ Paper    │ id, title, authors, abstract  │
│   │                                │ ChatMsg  │ id, role, content, ws_id     │
│   │                                └──────────┴──────────────────────────────┘
│   │
│   ├── 📂 routers/                  URL routes — like pages of a website
│   │   ├── 🔐 auth.py               Handles registration and login
│   │   │                            POST /auth/register → creates user in DB
│   │   │                            POST /auth/login    → returns JWT token
│   │   │
│   │   ├── 📄 papers.py             Handles paper management
│   │   │                            GET  /papers/workspaces       → list workspaces
│   │   │                            POST /papers/workspaces       → create workspace
│   │   │                            GET  /papers/search?query=... → hits arXiv API
│   │   │                            POST /papers/import           → saves to SQLite
│   │   │                            DELETE /papers/{id}           → removes paper
│   │   │
│   │   └── 🤖 chat.py               Handles AI conversations
│   │                                POST   /chat/                     → main Q&A
│   │                                GET    /chat/summarize/{id}        → summarize
│   │                                POST   /chat/compare              → compare
│   │                                GET    /chat/findings/{id}        → findings JSON
│   │                                GET    /chat/{ws_id}/history      → load history
│   │                                DELETE /chat/{ws_id}/history      → clear history
│   │
│   └── 📂 utils/                    AI brain — the smart part
│       ├── 🤖 groq_client.py        Creates Groq connection, sends prompts to
│       │                            Llama 3.3 70B, returns text responses
│       │
│       ├── 🧬 vector_db.py          Converts text → 384-number vectors
│       │                            Computes cosine similarity between vectors
│       │                            find_relevant_papers() → returns top-K papers
│       │
│       └── ⭐ research_assistant.py  All 5 AI agent functions (Milestone 5)
│                                    See "AI Agent" section below for details
│
└── ⚛️  frontend/                    Everything the USER SEES in the browser
    │
    ├── 🌐 .env                      REACT_APP_API_URL=http://localhost:8000
    ├── 📋 package.json              JS dependencies: react, axios, typescript, etc.
    ├── 🎨 tailwind.config.js        Custom colors: ink, brand-blue, brand-green, etc.
    │
    ├── 📂 public/
    │   └── 🏠 index.html            Single HTML page React mounts into
    │                                Has dark background to prevent white flash
    │
    └── 📂 src/                      All React source code
        │
        ├── 🚀 index.tsx             Launches React, renders <App/> into index.html
        ├── 💅 index.css             Global styles: dark background, scrollbar, fonts
        ├── 🗺️  App.tsx               Root layout:
        │                            ┌─────────────────────────────────┐
        │                            │  Header (logo + tabs + sign out)│
        │                            ├──────────┬──────────────────────┤
        │                            │ Sidebar  │ Main content area    │
        │                            │(Workspace│ (Papers OR Chatbot)  │
        │                            │ list)    │                      │
        │                            └──────────┴──────────────────────┘
        │
        ├── 📡 api.ts                ALL API functions in one file
        │                            Auto-attaches JWT header to every request
        │                            Auto-redirects to login on 401 errors
        │
        └── 📂 components/           Reusable UI blocks
            ├── 🔑 Login.tsx         Register/Login form with validation
            ├── 📁 Workspace.tsx     Sidebar: list workspaces, create new, select
            ├── 🔍 SearchPapers.tsx  Tab 1: search arXiv + My Library view
            └── 💬 Chatbot.tsx       Tab 2: chat bubbles, typing animation, suggestions
```
<br/>
