import instaloader
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

# Pydantic model for the request body to capture Instagram username
class UsernameRequest(BaseModel):
    username: str

# Function to check Instagram account based on profile details
def check_instagram_account(username):
    L = instaloader.Instaloader()

    try:
        # Load profile using the username
        profile = instaloader.Profile.from_username(L.context, username)

        # Example checks
        has_profile_picture = profile.profile_pic_url != 'https://instagram.fdel1-1.fna.fbcdn.net/v/t51.2885-19/10697377_442903424833709_262138144_a.jpg'
        num_posts = profile.mediacount
        followers = profile.followers
        following = profile.followees

        # Fake account criteria (these can be adjusted)
        fake_threshold = {
            'followers': 100,  # Minimum number of followers
            'posts': 5,        # Minimum number of posts
            'engagement_ratio': 0.02,  # Engagement ratio: (likes + comments) / followers
        }

        # Analyze if the account looks fake
        if not has_profile_picture or num_posts < fake_threshold['posts'] or followers < fake_threshold['followers']:
            return "This account seems suspicious or fake."

        # Further engagement checks could go here
        # For example: Calculate engagement rate using likes and comments on posts

        return "This account seems real."

    except instaloader.exceptions.ProfileNotExistsException:
        return "Account does not exist."
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Home route that serves the frontend HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r") as f:
        return f.read()

# API endpoint to receive username and check if it's a fake account or not
@app.post("/check_account/")
async def check_account(data: UsernameRequest):
    result = check_instagram_account(data.username)
    return {"result": result}
