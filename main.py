from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import instaloader
import requests

app = FastAPI()

# Define the InstagramRequest model to accept the username in the request body
class InstagramRequest(BaseModel):
    username: str

# Define the route to verify the Instagram account
@app.post("/verify_account/")
async def verify_account(request: InstagramRequest):
    try:
        # Initialize Instaloader
        loader = instaloader.Instaloader()

        # Fetch the profile using the provided username
        profile = instaloader.Profile.from_username(loader.context, request.username)

        # Check if the profile is private
        if profile.is_private:
            return {"status": "Account is private", "is_fake": False}

        # If the profile is public, verify authenticity using followers count (sample logic)
        if profile.followers < 100:  # Example: threshold followers count for checking authenticity
            return {"status": "Account seems suspicious (low followers)", "is_fake": True}

        # If the account is public and has a reasonable number of followers
        return {"status": "Account is verified", "is_fake": False}

    except Exception as e:
        # If any exception occurs, return a 404 error with the message
        raise HTTPException(status_code=404, detail=f"Error verifying account: {str(e)}")
