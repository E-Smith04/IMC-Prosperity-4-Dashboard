from fastapi import FastAPI
from data_platform.app.routers import historical, logs

app = FastAPI()

app.include_router(historical.router)
app.include_router(logs.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)