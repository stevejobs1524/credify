from fastapi import FastAPI, HTTPException
import instaloader

app = FastAPI()

# Initialize Instaloader
L = instaloader.Instaloader()

@app.get("/")
def read_root():
    return {"message": "Welcome to Instagram Fake Account Checker"}

@app.get("/check_instagram/{username}")
def check_instagram_account(username: str):
    try:
        # Load the profile
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Gather some details about the profile
        followers = profile.followers
        following = profile.followees
        posts = profile.mediacount
        bio = profile.biography
        is_private = profile.is_private
        is_verified = profile.is_verified
        
        # Basic checks for fake accounts
        if followers < 50 or posts < 10:
            result = "Likely Fake: Low followers or few posts."
        elif is_private and not is_verified:
            result = "Likely Fake: Private and unverified account."
        elif followers > 1000 and posts > 50 and not is_private and not is_verified:
            result = "Could be Fake: High followers but not verified and public."
        else:
            result = "Seems Legit: Profile has decent followers and posts."
        
        return {
            "username": username,
            "followers": followers,
            "following": following,
            "posts": posts,
            "bio": bio,
            "is_private": is_private,
            "is_verified": is_verified,
            "result": result
        }
    
    except instaloader.exceptions.ProfileNotExistsException:
        raise HTTPException(status_code=404, detail="Profile not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

