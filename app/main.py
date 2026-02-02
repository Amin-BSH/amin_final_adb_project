import uvicorn

if __name__ == "__main__":
    # Alert!!! take care about the reload
    uvicorn.run(app="config:app", host="127.0.0.1", port=8000, reload=True)
