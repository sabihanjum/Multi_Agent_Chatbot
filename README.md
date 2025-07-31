# 🧠 Multi-Agentic Chatbot (Text + Image AI Agent)

This project demonstrates a **multi-agent chatbot** system built with **Streamlit**, integrating **AWS Bedrock** models like Claude 3 Sonnet (for vision + text) and Stable Diffusion (for image generation). Enhanced with Lottie animations for an engaging UI.

---

## 🔍 What It Does

- Accepts **text + image inputs**
- Answers questions about uploaded images
- Generates new images from text prompts
- Maintains multi-turn **chat context**

---

## 🧰 Tech Stack

- **Frontend**: Streamlit + Lottie
- **Backend**: AWS Bedrock (Claude 3 Sonnet, Stable Diffusion)
- **Languages**: Python
- **Environment**: `.env` for secrets

---

## ⚙️ Getting Started

**Clone the repository**

```bash
git clone https://github.com/sabihanjum/multi-agentic-chatbot
cd multi-agentic-chatbot
Install dependencies

pip install -r requirements.txt

Create a .env file:
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=your-region

Run the app
streamlit run app.py
