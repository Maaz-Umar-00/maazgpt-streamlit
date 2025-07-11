import streamlit as st
import requests
import time

# === Load API Keys from secrets ===
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
STARRYAI_API_KEY = st.secrets["STARRYAI_API_KEY"]

st.set_page_config(page_title="MaazGPT", page_icon="🤖")
st.title("🧠 MaazGPT – AI Chatbot & Image Generator")

mode = st.radio("Choose mode:", ["💬 Text Generation", "🎨 Image Generation"])

user_input = st.text_area("Enter your prompt")

if st.button("Generate"):
    if mode == "💬 Text Generation":
        with st.spinner("Generating reply..."):
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "distil-whisper-large-v3-en",
                    "messages": [
                        {"role": "system", "content": "You are MaazGPT, created by Maaz Umar. Reply concisely."},
                        {"role": "user", "content": user_input}
                    ]
                }
            )
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            st.success("MaazGPT says:")
            st.write(reply)

    else:
        with st.spinner("Generating image..."):
            creation = requests.post(
                "https://api.starryai.com/creations/",
                headers={
                    "X-API-Key": STARRYAI_API_KEY,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                json={
                    "prompt": user_input,
                    "model": "lyra",
                    "aspectRatio": "square",
                    "images": 1
                }
            ).json()
            creation_id = str(creation["id"])

            # Polling loop
            image_url = None
            for attempt in range(10):
                st.write(f"🔁 Attempt {attempt+1}/10")
                time.sleep(5)
                status = requests.get(
                    f"https://api.starryai.com/creations/{creation_id}",
                    headers={"X-API-Key": STARRYAI_API_KEY}
                ).json()
                if status["status"] == "completed" and "images" in status:
                    image_url = status["images"][0]["url"]
                    break

            if image_url:
                st.image(image_url, caption="Generated Image")
                st.download_button("Download Image", requests.get(image_url).content, "maazgpt_image.png")
            else:
                st.error("❌ Image generation failed or timed out.")
