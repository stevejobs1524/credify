from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import instaloader

app = FastAPI()

# Define input format
class Username(BaseModel):
    username: str

# Initialize instaloader
L = instaloader.Instaloader()

def check_account(username: str) -> dict:
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        
        # You can add more checks based on profile attributes
        account_data = {
            'username': profile.username,
            'followers': profile.followers,
            'posts': profile.mediacount,
            'is_private': profile.is_private,
            'is_verified': profile.is_verified,
            'profile_pic': profile.profile_pic_url,
        }
        
        # Basic check for fake accounts
        if profile.followers < 100 or profile.mediacount < 5:
            return {'status': 'Fake', 'details': account_data}
        return {'status': 'Real', 'details': account_data}
    
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found or error with Instagram data")

# Define endpoint to verify Instagram account
@app.post("/verify")
async def verify_account(username: Username):
    result = check_account(username.username)
    return result
