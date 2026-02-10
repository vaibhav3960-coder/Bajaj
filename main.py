from fastapi import FastAPI, HTTPException
from math import gcd
from functools import reduce
import os
from google import genai
from pydantic import BaseModel
from typing import Optional, List, Any

# ---------- Gemini setup (Latest google-genai format) ----------
# Make sure to install the new SDK: pip install google-genai
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

EMAIL = "vaibhav3960.beai23@chitkara.edu.in"

# ---------- Helper functions ----------

def fibonacci(n):
    # Handle negative or zero input gracefully
    if n <= 0:
        return []
    a, b = 0, 1
    res = []
    for _ in range(n):
        res.append(a)
        a, b = b, a + b
    return res

def is_prime(x):
    # Handle non-integers or small numbers
    if not isinstance(x, int) or x < 2:
        return False
    for i in range(2, int(x**0.5) + 1):
        if x % i == 0:
            return False
    return True

def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)

def lcm_list(arr):
    if not arr:
        return 0
    return reduce(lcm, arr)

def hcf_list(arr):
    if not arr:
        return 0
    return reduce(gcd, arr)

# ---------- APIs ----------

@app.get("/health")
def health():
    return {
        "is_success": True,
        "official_email": EMAIL
    }

@app.post("/bfhl")
def bfhl(payload: dict):
    try:
        data = None
        
        if "fibonacci" in payload:
            try:
                n = int(payload["fibonacci"])
                data = fibonacci(n)
            except ValueError:
                 raise HTTPException(status_code=400, detail="Invalid fibonacci number")

        elif "prime" in payload:
            arr = payload["prime"]
            if not isinstance(arr, list):
                 raise HTTPException(status_code=400, detail="Prime input must be a list")
            data = [x for x in arr if is_prime(x)]

        elif "lcm" in payload:
            arr = payload["lcm"]
            if not isinstance(arr, list):
                 raise HTTPException(status_code=400, detail="LCM input must be a list")
            data = lcm_list(arr)

        elif "hcf" in payload:
            arr = payload["hcf"]
            if not isinstance(arr, list):
                 raise HTTPException(status_code=400, detail="HCF input must be a list")
            data = hcf_list(arr)

        elif "AI" in payload:
            q = payload["AI"]
            try:
                # Switched to gemini-1.5-flash for better free tier stability
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=q
                )
                data = response.text.strip()
            except Exception as e:
                # Catch 429 errors specifically to return a clean message
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    raise HTTPException(
                        status_code=429, 
                        detail="Google AI Quota Exceeded. Please try again later."
                    )
                # Re-raise other exceptions to be caught by the outer block
                raise e

        else:
            raise HTTPException(status_code=400, detail="Invalid input: No supported key found")

        return {
            "is_success": True,
            "official_email": EMAIL,
            "data": data
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        # Log the actual error for debugging
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Processing error")