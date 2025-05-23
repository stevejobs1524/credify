from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Pydantic model to structure input data
class UsernameRequest(BaseModel):
    username: str

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Hello, world! Welcome to the CrediFy backend!"}

# Endpoint to check if the username is fake or real (dummy check for now)
@app.post("/check")
def check_fake_account(request: UsernameRequest):
    username = request.username

    # Dummy logic for checking a fake account (replace with actual logic later)
    if "fake" in username.lower():
        return {"username": username, "status": "fake"}
    else:
        return {"username": username, "status": "real"}

