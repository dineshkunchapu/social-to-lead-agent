# Social-to-Lead Agentic Workflow

## 📌 Overview
This project implements a **GenAI-powered conversational agent** for a fictional SaaS product **AutoStream**, built as part of the **Machine Learning Intern assignment for ServiceHive (Inflx platform)**.

The agent is designed to convert user conversations into qualified business leads by:
- Understanding user intent
- Answering product and pricing questions accurately using RAG
- Identifying high-intent users
- Safely triggering backend actions such as lead capture

---

## 🎯 Problem Statement
AutoStream is a SaaS platform that provides automated video editing tools for content creators.

The goal of this agent is to:
- Handle product and pricing inquiries
- Detect users who are ready to sign up
- Capture lead information in a structured, real-world manner

---

## 🧠 Agent Capabilities

### 1️⃣ Intent Identification
The agent classifies user messages into three intent categories using a **GenAI model (Google Gemini)**:
- **CASUAL** – greetings or general conversation
- **PRODUCT_QUERY** – questions about pricing, plans, or features
- **HIGH_INTENT** – user expresses readiness to try or sign up

Intent detection controls the flow of the conversation and determines when to initiate lead qualification.

---

### 2️⃣ RAG-Powered Knowledge Retrieval
The agent uses **Retrieval-Augmented Generation (RAG)** to answer user questions by grounding responses in a **local knowledge base** stored as JSON.

The knowledge base includes:
- AutoStream pricing and plan details
- Company policies (refunds and support availability)

This approach ensures accurate, non-hallucinated responses.

---

### 3️⃣ Stateful Conversation
The agent maintains conversational state across multiple turns, tracking:
- Current intent
- User name
- Email address
- Creator platform (YouTube, Instagram, etc.)

State management ensures the conversation progresses logically and prevents premature backend actions.

---

### 4️⃣ Tool Execution – Lead Capture
When a user shows high intent, the agent:
1. Collects name
2. Collects email
3. Collects creator platform

Only after **all required details are collected**, the agent triggers a mock backend function to simulate lead capture.

This mirrors real-world production safeguards.

---

## 🏗️ Architecture Overview

User Message
↓
Intent Detection (Gemini)
↓
RAG Knowledge Retrieval (Local JSON)
↓
High-Intent Qualification
↓
Lead Detail Collection
↓
Mock Lead Capture Tool


---

## ⚙️ Tech Stack
- **Language:** Python 3
- **LLM:** Google Gemini API
- **Knowledge Base:** Local JSON (RAG)
- **State Management:** In-memory state dictionary
- **Tooling:** Mock backend function for lead capture
- **Interface:** CLI-based conversational agent

---

## ▶️ How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/social-to-lead-agent.git
cd social-to-lead-agent
2️⃣ Set Google API key

Set your Gemini API key as an environment variable.
3️⃣ Run the agent
python app.py

💬 Sample Conversation Flow
User: Hi, tell me about pricing
Agent: AutoStream Pricing:
       - Basic Plan: $29/month, 10 videos/month, 720p
       - Pro Plan: $79/month, Unlimited videos, 4K, AI captions

User: I want to try the Pro plan for my YouTube channel
Agent: Great! May I know your name?

User: Dinesh
Agent: Thanks! What's your email?

User: dinesh@gmail.com
Agent: Which platform do you create content on?

User: YouTube
Agent: Lead captured successfully
