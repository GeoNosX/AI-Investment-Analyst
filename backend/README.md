# 🔬 AI Multi-Agent Research Assistant

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/ci.yml)

An autonomous, multi-agent AI research system that dynamically generates a team of specialized AI experts to investigate any given topic. Built with LangGraph and powered by Meta's Llama 3.1 70B, the agents conduct independent web searches, compile their findings, and synthesize a massive, multi-perspective final report.

## 🚀 Features

* **Dynamic AI Personas:** Input a topic, and the system automatically generates a customized team of researchers with unique roles, backgrounds, and perspectives.
* **Autonomous Web Research:** Agents utilize Google Serper, Tavily, and Wikipedia to hunt down real-time, factual information.
* **Multi-Perspective Synthesis:** The system aggregates individual agent reports into one comprehensive master document.
* **Fully Containerized:** Runs flawlessly on any machine using Docker and Docker Compose.
* **Automated CI/CD:** Protected by GitHub Actions with automated Pytest runs and Docker build verifications.

## 🛠️ Tech Stack

* **Frontend:** Vanilla HTML, CSS, JavaScript (served via Nginx)
* **Backend:** Python 3.11, FastAPI, Uvicorn
* **AI Orchestration:** LangGraph, LangChain
* **LLM:** Meta Llama 3.1 70B Instruct (via Nvidia Inference API)
* **Tools:** Google Serper API, Tavily Search API, Wikipedia
* **Infrastructure:** Docker, Docker Compose, GitHub Actions

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Git

You will also need API keys for the following services:
* **Nvidia API** (For Llama 3.1 inference)
* **Tavily API** (For AI-optimized search)
* **Serper API** (For Google Search results)

## ⚙️ Installation & Setup

**1. Clone the repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME

**2. Set up your Environment Variables:**

Create a .env file in the root directory and add your API keys:

NVIDIA_API_KEY=your_nvidia_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
SERPER_API_KEY=your_serper_api_key_here

