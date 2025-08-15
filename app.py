import streamlit as st
import requests, time, json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

st.set_page_config(page_title="MaazGPT", page_icon="🤖")
st.title("🧠 MaazGPT – AI Chatbot & Image Generator")

# --- Secrets sanity check ---
missing = [k for k in ("GROQ_API_KEY","STARRYAI_API_KEY") if k not in st.secrets]
if missing:
    st.error(f"Missing secrets: {', '.join(missing)} (add them in Secrets)")
    st.stop()

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
STARRYAI_API_KEY = st.secrets["STARRYAI_API_KEY"]

# --- Robust HTTP session with retries & timeouts ---
def make_session():
    s = requests.Session()
    retries = Retry(
        total=5, connect=5, read=5, backoff_factor=0.6,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET","POST"])
    )
    s.headers.update({"User-Agent": "MaazGPT/1.0 (+streamlit)"})
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    return s

session = make_session()

mode = st.radio("Choose mode:", ["💬 Text Generation", "🎨 Image Generation"])
user_input = st.text_area("Enter your prompt")

if st.button("Generate"):
    if not user_input.strip():
        st.warning("Please enter a prompt.")
        st.stop()

    if mode == "💬 Text Generation":
        with st.spinner("Generating reply..."):
            try:
                resp = session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "gemma2-9b-it",
                        "messages": [
                            {"role": "system", "content": "You are MaazGPT, created by Maaz Umar. Reply concisely."},
                            {"role": "user", "content": user_input}
                        ],
                    },
                    timeout=30,
                )
                resp.raise_for_status()
                data = resp.json()
                reply = data["choices"][0]["message"]["content"]
                st.success("MaazGPT says:")
                st.write(reply)
            except requests.HTTPError as e:
                st.error(f"Groq API HTTP error: {e.response.status_code} – {e.response.text[:300]}")
            except requests.RequestException as e:
                st.error("Network error while calling Groq.")
                st.exception(e)

    else:
        with st.spinner("Generating image..."):
            try:
                # --- Kick off creation ---
                creation_resp = session.post(
                    "https://api.starryai.com/creations/",
                    headers={
                        "X-API-Key": STARRYAI_API_KEY,
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                    },
                    json={
                        "prompt": user_input,
                        "model": "lyra",          # per StarryAI docs
                        "aspectRatio": "square",
                        "images": 1
                    },
                    timeout=30,
                )
                creation_resp.raise_for_status()
                creation = creation_resp.json()
                creation_id = str(creation.get("id", ""))  # defensive
                if not creation_id:
                    st.error(f"StarryAI returned no creation id. Raw: {json.dumps(creation)[:400]}")
                    st.stop()

                # --- Poll for result with backoff ---
                image_url = None
                for attempt in range(1, 16):  # up to ~75s
                    st.write(f"🔁 Attempt {attempt}/15")
                    time.sleep(min(5 + attempt, 10))
                    status_resp = session.get(
                        f"https://api.starryai.com/creations/{creation_id}",
                        headers={"X-API-Key": STARRYAI_API_KEY, "Accept": "application/json"},
                        timeout=30,
                    )
                    status_resp.raise_for_status()
                    status = status_resp.json()
                    if status.get("status") == "completed" and status.get("images"):
                        image_url = status["images"][0].get("url")
                        break
                    if status.get("status") in {"failed","error"}:
                        st.error(f"StarryAI reported failure: {json.dumps(status)[:400]}")
                        st.stop()

                if image_url:
                    # download then display to avoid mixed-content or hotlink issues
                    bin_img = session.get(image_url, timeout=30).content
                    st.image(bin_img, caption="Generated Image")
                    st.download_button("Download Image", bin_img, "maazgpt_image.png")
                else:
                    st.error("❌ Image generation didn’t complete in time. Try again or tweak the prompt.")

            except requests.HTTPError as e:
                st.error(f"StarryAI HTTP error: {e.response.status_code} – {e.response.text[:300]}")
            except requests.RequestException as e:
                st.error("Network/connection error while calling StarryAI.")
                st.info("Tip: Open the app’s **Manage app → Logs** to see the underlying socket/TLS error.")
                st.exception(e)

