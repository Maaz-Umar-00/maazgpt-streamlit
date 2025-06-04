
# 🧠 MaazGPT – Streamlit AI Chatbot with Image & Text Generation

Welcome to **MaazGPT**, a lightweight AI chatbot built using **Streamlit**, powered by **Groq (LLM)** for text generation and **StarryAI** for image generation. This project allows users to:
- Chat interactively with AI (like ChatGPT)
- Generate AI images from prompts
- Easily swap in their own API keys

---

## 🚀 Features

- 🧠 **Text Generation** via Groq's `llama3-70b-8192`
- 🎨 **Image Generation** via StarryAI
- 💬 User-friendly **Streamlit Web Interface**
- 🔐 Secure API key management via `.streamlit/secrets.toml`
- 🌐 Deployable to Streamlit Cloud (Free Hosting!)



---

## 🛠️ Installation (Run Locally)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Maaz-Umar-00/maazgpt-streamlit.git
   cd maazgpt-streamlit
   ```

2. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API keys**  
   Create a file: `.streamlit/secrets.toml`

   ```toml
   # .streamlit/secrets.toml

   groq_api_key = "your_groq_api_key"
   starryai_api_key = "your_starryai_api_key"
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## 🧠 How It Works

### 🔹 Text Generation
Uses the Groq API (compatible with OpenAI format) and LLaMA3-70B model to handle user queries.

### 🔹 Image Generation
Uses the StarryAI API to send prompts and poll for generated images, which are then displayed and can be downloaded.

---

## 🧑‍💻 Customize with Your Own API Keys

- **Groq API**  
  Sign up and get a key from: [https://console.groq.com](https://console.groq.com)

- **StarryAI API**  
  Get free credits at: [https://starryai.readme.io](https://starryai.readme.io)

- Add these keys in the `.streamlit/secrets.toml` file (as shown above).

---

## 🌍 Deploy on Streamlit Cloud

1. Push your project to a **public GitHub repo**
2. Go to: [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Sign in and click **"New App"**
4. Select your repo and set the **`app.py`** as the main file
5. Add your API keys under `Secrets` section:
   ```toml
   groq_api_key = "your_groq_api_key"
   starryai_api_key = "your_starryai_api_key"
   ```

---

## 📂 Project Structure

```text
maazgpt-streamlit/
│
├── app.py                       # Main Streamlit app
├── requirements.txt             # Required packages
├── .streamlit/
│   └── secrets.toml             # API Keys (not pushed to GitHub)
├── utils/
│   ├── groq_utils.py            # Handles text completion
│   └── starryai_utils.py        # Handles image generation
```

---

## 🙋‍♂️ Author

**Maaz Umar**  
- LinkedIn: [maaz-umar](https://www.linkedin.com/in/maaz-umar-)  
- GitHub: [Maaz-Umar-00](https://github.com/Maaz-Umar-00)

---


---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and share it!
