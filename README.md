# Automated Financial News Cognition & Alert Pipeline

##  Project Overview
This project is an end-to-end, fully localized automated data pipeline designed to ingest, process, and analyze financial news in real-time. By orchestrating workflow automation with local Large Language Models (LLMs), the system extracts multidimensional financial insights from raw news articles and delivers targeted market alerts.

##  System Architecture & Tech Stack
The pipeline operates entirely on a localized, containerized environment to ensure maximum data privacy and eliminate API dependencies.

* **Workflow Orchestration:** `n8n` (Dockerized)
* **Data Ingestion:** Web scraping via `n8n` HTTP Request & HTML nodes targeting financial news portals.
* **AI Engine / NLP:** Local LLM (`Qwen-2.5` via `Ollama`)
* **Database Engine:** `PostgreSQL`
* **Evaluation Engine:** `Python` (pandas, scikit-learn)
* **Notification Layer:** `Telegram Bot API` & `SMTP Email`

##  Core Workflow
1.  **Target Selection:** Reads active stock tickers from a centralized Google Sheet.
2.  **Scraping & Pre-processing:** Fetches $T-1$ articles, parses DOM structures, and consolidates texts into a token-optimized JSON structure.
3.  **Cognitive Extraction:** The `Qwen-2.5` model extracts exactly 6 fields: *Market Sentiment, Event Category, Financial Metric, Growth Catalyst, Risk Warning, and AI Action Signal*.
4.  **Database Storage:** Extracted metrics are parsed and logged into a relational `PostgreSQL` database.
5.  **Dual-Stream Delivery:** * **Stream 1:** Critical/High-impact news triggers real-time Telegram alerts.
    * **Stream 2:** A comprehensive daily market digest is compiled and emailed to the user.

##  Empirical Validation
Before production deployment, the extraction capabilities of the local LLM were quantitatively tested. A sample dataset of 60 financial articles was manually annotated for sentiment (Positive, Neutral, Negative) and cross-referenced against the model's outputs using Python, ensuring high reliability in the extraction layer.

##  How to Run Locally

### Prerequisites
* [Docker](https://www.docker.com/) & Docker Compose
* [Ollama](https://ollama.com/) installed locally with the `qwen2.5` model pulled (`ollama run qwen2.5`)

### Setup Instructions
1. Clone this repository:
   ```bash
   git clone [https://github.com/toanthiennguyen2005-alt/n8n-financial-alarm](https://github.com/toanthiennguyen2005-alt/n8n-financial-alarm)
   cd n8n-financial-alarm
Start the infrastructure (n8n & PostgreSQL) via Docker:

Bash
docker-compose up -d
Import the n8n_workflow.json file into your local n8n instance.

Update the Google Sheets credentials, Telegram Bot API, and Email SMTP settings within the n8n nodes.
