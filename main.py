from fastapi import FastAPI, HTTPException
from instaloader import Instaloader, Profile


app = FastAPI()

SESSION_FILE = "YOUR_SESSION_FILE" 
LIMIT = 100 


def load_instaloader():
    loader = Instaloader()
    try:
        loader.load_session_from_file(SESSION_FILE)
        return loader
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Session load failed: {e}")


def fetch_ig_data(username: str, data_type: str):
    loader = load_instaloader()
    try:
        profile = Profile.from_username(loader.context, username)

        if data_type == "followers":
            data = [f.username for _, f in zip(range(LIMIT), profile.get_followers())]
        elif data_type == "following":
            data = [f.username for _, f in zip(range(LIMIT), profile.get_followees())]
        else:
            raise HTTPException(status_code=400, detail="Invalid data type requested")

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Instagram fetch error: {e}")


@app.get("/followers/{username}")
async def get_followers(username: str):
    data = fetch_ig_data(username, "followers")
    return {"username": username, "followers": data}


@app.get("/following/{username}")
async def get_following(username: str):
    data = fetch_ig_data(username, "following")
    return {"username": username, "following": data}
