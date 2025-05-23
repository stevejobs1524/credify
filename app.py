import instaloader
from fastapi import FastAPI
from pydantic import BaseModel
import torch
from torch_geometric.data import Data

app = FastAPI()

# Create the model class for input validation
class InstagramUsername(BaseModel):
    username: str

# Initialize Instaloader
L = instaloader.Instaloader()

def get_instagram_data(username: str):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        followers = profile.followers
        following = profile.followees
        post_count = profile.mediacount
        bio = profile.biography
        is_private = profile.is_private
        return {
            "followers": followers,
            "following": following,
            "post_count": post_count,
            "bio": bio,
            "is_private": is_private
        }
    except Exception as e:
        return {"error": str(e)}

# Fake account detection logic
def evaluate_fake_account(data):
    # Dummy model: this should be replaced by your actual model logic
    if data["followers"] < 100 or data["following"] > 5000:
        return True
    return False

@app.post("/evaluate")
async def evaluate_account(account: InstagramUsername):
    # Fetch Instagram profile data
    profile_data = get_instagram_data(account.username)

    if "error" in profile_data:
        return {"error": "Failed to fetch profile data"}

    # Evaluate whether the account is fake or not
    is_fake = evaluate_fake_account(profile_data)
    
    return {"username": account.username, "is_fake": is_fake, "profile_data": profile_data}
