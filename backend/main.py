import base64
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="Image-to-Prompt Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STYLE_INSTRUCTIONS = {
    "descriptive": "Write a vivid, detailed visual description of the image.",
    "casual": "Describe the image in a casual, natural, easy-to-read way.",
    "straightforward": "Describe the image clearly and directly with no extra flourish.",
    "stable_diffusion": "Convert the image into a Stable Diffusion prompt using comma-separated prompt terms.",
    "midjourney": "Convert the image into a MidJourney-style prompt with strong visual composition language.",
    "e621": "Convert the image into an e621-style tag list using comma-separated tags only."
}

LENGTH_INSTRUCTIONS = {
    "any": "Use whatever length is appropriate.",
    "very_short": "Keep it extremely brief.",
    "short": "Keep it short.",
    "medium": "Use a medium-length response.",
    "long": "Use a long, detailed response.",
    "very_long": "Use a very long and highly detailed response."
}

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/generate")
async def generate_prompt(
    image: UploadFile = File(...),
    style: str = Form("descriptive"),
    length: str = Form("medium"),
    max_words: int | None = Form(None)
):
    image_bytes = await image.read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    mime_type = image.content_type or "image/png"

    style_instruction = STYLE_INSTRUCTIONS.get(style, STYLE_INSTRUCTIONS["descriptive"])
    length_instruction = LENGTH_INSTRUCTIONS.get(length, LENGTH_INSTRUCTIONS["medium"])

    word_limit_instruction = ""
    if max_words:
        word_limit_instruction = f"Do not exceed {max_words} words."

    system_prompt = f"""
You are an image-to-prompt generator.

Analyze the uploaded image and produce one output based on the selected format.

Style mode:
{style_instruction}

Length mode:
{length_instruction}

{word_limit_instruction}

Rules:
- Describe only visible image content.
- Do not invent unseen context.
- Include subject, pose, clothing, expression, setting, lighting, mood, color palette, camera angle, and composition when relevant.
- For Stable Diffusion, prioritize useful generation keywords.
- For MidJourney, write a polished generation prompt.
- For e621, output tags only.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": system_prompt
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:{mime_type};base64,{encoded_image}"
                    }
                ]
            }
        ]
    )

    return {
        "prompt": response.output_text
    }
