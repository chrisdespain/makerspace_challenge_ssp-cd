from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import hmac
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS so the frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/api/access")
def access(x_access_code: str | None = Header(default=None)):
    # Lets the frontend show a proactive gate without knowing server config:
    # reports whether a code is required and whether the supplied one is valid.
    # Never returns the code itself. Real enforcement stays on POST /api/chat.
    expected_code = os.getenv("APP_ACCESS_CODE")
    required = bool(expected_code)
    valid = (not required) or (
        x_access_code is not None and hmac.compare_digest(x_access_code, expected_code)
    )
    return {"required": required, "valid": valid}

@app.post("/api/chat")
def chat(request: ChatRequest, x_access_code: str | None = Header(default=None)):
    # Access gate: when APP_ACCESS_CODE is configured (e.g. in production), the
    # request must carry a matching X-Access-Code header. With no APP_ACCESS_CODE
    # set (local dev), the gate is open so local development needs no code.
    expected_code = os.getenv("APP_ACCESS_CODE")
    if expected_code and not (
        x_access_code and hmac.compare_digest(x_access_code, expected_code)
    ):
        raise HTTPException(status_code=401, detail="Invalid or missing access code")

    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    
    try:
        user_message = request.message
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a supportive mental coach, but you have a terrible attitude. All of your responses should be sarcastic."},
                {"role": "user", "content": user_message}
            ]
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")
