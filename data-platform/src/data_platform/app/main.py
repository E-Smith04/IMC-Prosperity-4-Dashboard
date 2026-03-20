from fastapi import FastAPI
from data_platform.app.routers import prices, trades

app = FastAPI()

app.include_router(prices.router)
app.include_router(trades.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)