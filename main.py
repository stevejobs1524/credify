from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import instaloader
import requests

app = FastAPI()

class InstagramRequest(BaseModel):
    username: str

@app.post("/verify_account/")
async def verify_account(request: InstagramRequest):
    try:
        # Initialize Instaloader
        loader = instaloader.Instaloader()

        # Fetch the profile using the provided username
        profile = instaloader.Profile.from_username(loader.context, request.username)

        # Check if the profile has a valid 'is_private' attribute
        if profile.is_private:
            return {"status": "Account is private", "is_fake": False}

        # If the profile is public, verify authenticity using followers count (sample logic)
        if profile.followers < 100:  # Example: threshold followers count for checking authenticity
            return {"status": "Account seems suspicious (low followers)", "is_fake": True}

        return {"status": "Account is verified", "is_fake": False}

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error verifying account: {str(e)}")

