import uvicorn

if __name__ == "__main__":
    # Alert!!! take care about the reload
    uvicorn.run(app="config:app", host="0.0.0.0", port=8080, reload=True)
