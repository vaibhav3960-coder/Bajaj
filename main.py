from fastapi import FastAPI, HTTPException
from math import gcd
from functools import reduce
import requests
import google.generativeai as genai
genai.configure(api_key="AIzaSyA4qVWX5sE8BSch4LYA3HyHn3Ufsuu5tC0")
model = genai.GenerativeModel("gemini-pro")


app = FastAPI()

EMAIL = "vaibhav3960.beai23@chitkara.edu.in"


# ---------- Helper functions ----------

def fibonacci(n):
    if n <= 0:
        return []
    a, b = 0, 1
    res = []
    for _ in range(n):
        res.append(a)
        a, b = b, a + b
    return res

def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(x**0.5)+1):
        if x % i == 0:
            return False
    return True

def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_list(arr):
    return reduce(lcm, arr)

def hcf_list(arr):
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
        if "fibonacci" in payload:
            n = int(payload["fibonacci"])
            data = fibonacci(n)

        elif "prime" in payload:
            arr = payload["prime"]
            data = [x for x in arr if is_prime(x)]

        elif "lcm" in payload:
            data = lcm_list(payload["lcm"])

        elif "hcf" in payload:
            data = hcf_list(payload["hcf"])

        elif "AI" in payload:
            q = payload["AI"]
            response = model.generate_content(q)
            data = response.text.strip().split()[0]   # single word output


        else:
            raise HTTPException(status_code=400, detail="Invalid input")

        return {
            "is_success": True,
            "official_email": EMAIL,
            "data": data
        }

    except Exception:
        raise HTTPException(status_code=400, detail="Processing error")
