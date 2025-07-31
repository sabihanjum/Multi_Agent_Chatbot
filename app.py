import streamlit as st
import boto3
import base64
from PIL import Image
import io
import json
import requests
from streamlit_lottie import st_lottie

# ---------------------- Lottie Setup ----------------------
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animations (from local or replace with URL-based)
lottie_header = load_lottiefile("lottiefiles/coding2.json")
lottie_sidebar = load_lottiefile("lottiefiles/coding1.json")
# ----------------------------------------------------------

# Initialize AWS Bedrock runtime client
bedrock = boto3.client("bedrock-runtime")

# Claude Sonnet model ID
CLAUDE_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
# Stable Diffusion model ID
STABLE_DIFFUSION_MODEL_ID = "stability.stable-diffusion-xl-v1"

# Function to call Claude Sonnet for text or image understanding
def call_claude(prompt, image_bytes=None, context=[]):
    messages = context + [{"role": "user", "content": []}]
    if prompt:
        messages[-1]["content"].append({"type": "text", "text": prompt})
    if image_bytes:
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
        messages[-1]["content"].append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": encoded_image
            }
        })

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": messages,
        "max_tokens": 1024
    }

    response = bedrock.invoke_model(
        modelId=CLAUDE_MODEL_ID,
        body=json.dumps(body)
    )
    result = json.loads(response['body'].read())
    return result['content'][0]['text'], messages

# Function to call Stable Diffusion for image generation
def generate_image(prompt):
    body = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 10,
        "seed": 0,
        "steps": 50
    }

    response = bedrock.invoke_model(
        modelId=STABLE_DIFFUSION_MODEL_ID,
        body=json.dumps(body)
    )
    result = json.loads(response['body'].read())
    image_data = base64.b64decode(result['artifacts'][0]['base64'])
    return Image.open(io.BytesIO(image_data))

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="Multi-Agentic Chatbot", layout="wide")

# Header with Lottie
header_col1, header_col2 = st.columns([1, 5])
with header_col1:
    st_lottie(lottie_header, height=100, key="header")
with header_col2:
    st.title("Multi Agentic Chatbot 🤖🧠")

# Sidebar animation
with st.sidebar:
    st_lottie(lottie_sidebar, height=300, key="sidebar")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

text_input = st.text_input("Prompt:")
image_input = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if st.button("Submit"):
    image_bytes = image_input.read() if image_input else None
    context = st.session_state.chat_history

    if text_input and image_bytes:
        response, updated_context = call_claude(text_input, image_bytes, context)
        st.session_state.chat_history = updated_context + [{"role": "assistant", "content": [{"type": "text", "text": response}]}]
        st.image(Image.open(io.BytesIO(image_bytes)), caption="Uploaded Image", use_container_width=True)
        st.success("Bot: " + response)

    elif text_input and not image_bytes:
        if text_input.lower().startswith("generate image"):
            prompt = text_input.replace("generate image", "").strip()
            generated_image = generate_image(prompt)
            st.image(generated_image, caption="Generated Image", use_container_width=True)
            st.session_state.chat_history.append({"role": "user", "content": [{"type": "text", "text": text_input}]})
            st.session_state.chat_history.append({"role": "assistant", "content": [{"type": "text", "text": "Generated image based on your prompt."}]})
        else:
            response, updated_context = call_claude(text_input, None, context)
            st.session_state.chat_history = updated_context + [{"role": "assistant", "content": [{"type": "text", "text": response}]}]
            st.success("Bot: " + response)

    elif not text_input and image_bytes:
        response, updated_context = call_claude("", image_bytes, context)
        st.session_state.chat_history = updated_context + [{"role": "assistant", "content": [{"type": "text", "text": response}]}]
        st.image(Image.open(io.BytesIO(image_bytes)), caption="Uploaded Image", use_column_width=True)
        st.success("Bot: " + response)

# Display chat history
st.subheader("Chat History")
for message in st.session_state.chat_history:
    role = message["role"]
    for content in message["content"]:
        if content["type"] == "text":
            st.markdown(f"**{role.capitalize()}:** {content['text']}")
