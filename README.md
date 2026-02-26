# 🔬 NOVA · AI Data Intelligence

<div align="center">

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-A855F7?style=for-the-badge&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-00E5FF?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00FF88?style=for-the-badge)

### ⚡ Ask anything about your data. Get instant AI-powered analysis.

**[🚀 Live Demo → nova-ai-analyst.streamlit.app](https://nova-ai-analyst.streamlit.app)**

*Developed by **Kanav Chauhan***

</div>

---

## 📌 Overview

**NOVA** is a professional AI-powered data analyst built with Streamlit and Groq's LLaMA 3.3 70B. Upload any dataset and instantly get statistical insights, auto-generated visualizations, column profiling, and a conversational AI analyst — all in a sleek cyber-intelligence UI.

No SQL expertise needed. No data science background required. Just upload and ask.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 **Multi-format Upload** | CSV, XLSX, JSON — auto-detected and parsed |
| 📊 **Dataset Overview** | Live stats — rows, columns, nulls, duplicates, memory |
| 💡 **Auto Insights** | AI detects skew, correlations, missing data, high cardinality |
| 🔬 **Data Explorer** | Sortable, filterable preview with CSV download |
| 📈 **Chart Builder** | Bar, Line, Area, Scatter, Histogram — auto & custom |
| 🧬 **Data Profile** | Per-column stats, distributions, fill rate, unique counts |
| 🤖 **AI Analyst** | Ask plain-English questions → results + auto charts |
| ⚗️ **Query Engine** | SQL-like queries with AI explanation feature |
| 🎨 **Cyber UI** | Dark theme with animated gradients, floating effects, neon accents |

---

## 🛠️ Tech Stack

```
Frontend        →  Streamlit 1.41.1
AI Engine       →  Groq API (LLaMA 3.3 70B Versatile)
API Transport   →  Python requests (zero extra dependencies)
Data Engine     →  Pandas 2.1.4 + NumPy 1.26.4
Charts          →  Streamlit Native Charts
XLSX Parser     →  Custom zero-dependency parser (zipfile + xml)
Deployment      →  Streamlit Community Cloud
Fonts           →  Exo 2 · Space Mono · Inter (Google Fonts)
```

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-data-analyst.git
cd ai-data-analyst
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key

Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_your_key_here"
```
> Get your **free** API key at [console.groq.com](https://console.groq.com)

### 4. Run
```bash
streamlit run ai_data_analyst.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## ☁️ Deploy on Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **Create app**
3. Select repo, branch, and `ai_data_analyst.py` as main file
4. **Advanced settings → Secrets** → add:
```toml
GROQ_API_KEY = "gsk_your_key_here"
```
5. Click **Deploy** 🚀

---

## 📁 Project Structure

```
├── ai_data_analyst.py    # Main Streamlit application
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── LICENSE               # MIT License
└── .streamlit/
    └── secrets.toml      # API keys (DO NOT commit)
```

---

## 📦 Requirements

```
streamlit==1.41.1
pandas==2.1.4
numpy==1.26.4
openpyxl==3.1.2
```

---

## 🧠 How It Works

```
User uploads CSV / XLSX / JSON
          ↓
NOVA auto-profiles data:
  → Row/column counts, null detection, type inference
  → Skewness, correlations, cardinality analysis
          ↓
5 Analysis Tabs unlock:
  🔬 Data Explorer  →  Preview, sort, filter, download
  📈 Visualizations →  Auto + custom chart builder
  🧬 Data Profile   →  Per-column deep statistics
  🤖 AI Analyst     →  Plain English Q&A with Groq AI
  ⚗️ Query Engine   →  SQL-like queries + AI explanation
          ↓
AI Assistant uses full schema + sample data as context
User asks → Groq generates analysis → results shown instantly
```

---

## 💬 Example AI Queries

```
"Summarize this dataset"
"Which column has the most missing values?"
"Show top 10 rows sorted by salary"
"What are the key trends in this data?"
"Find all duplicate records"
"What's the average age by department?"
"Which category appears most frequently?"
```

---

## 🎨 UI Design

NOVA uses a **Cyber Intelligence** aesthetic:
- **Colors**: Electric cyan `#00E5FF` · Violet `#A855F7` · Neon green `#00FF88`
- **Fonts**: Exo 2 (headers) · Space Mono (data) · Inter (body)
- **Effects**: Animated gradient title, radial glow orbs, pulse animations
- **Cards**: Glassmorphism stat cards with neon border glow on hover

---

## ⚠️ Disclaimer

NOVA is an AI-powered analytical tool for informational purposes. AI-generated results should be **verified before use in critical decisions**. The developer assumes no liability for decisions made based on NOVA's output.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙌 Acknowledgements

- [Groq](https://groq.com) — Ultra-fast LLaMA 3.3 70B inference
- [Streamlit](https://streamlit.io) — Python web app framework
- [Meta LLaMA](https://llama.meta.com) — Open-source LLM
- [Google Fonts](https://fonts.google.com) — Exo 2, Space Mono, Inter

---

<div align="center">

**Developed by Kanav Chauhan**

⚡ [Try NOVA Live](https://nova-ai-analyst.streamlit.app)

</div>
