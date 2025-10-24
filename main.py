import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from database import engine, Base
from routers import orders, work_results
from routers import data_summary
from routers.weather import router as weather_router
from middlewares.logging_middleware import LoggingMiddleware
from middlewares.jwt_middleware import JWTMiddleware

# 로깅 설정
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MES Copilot Demo")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],  # 허용할 도메인
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(LoggingMiddleware)

# Add JWT middleware
# app.add_middleware(JWTMiddleware)


app.include_router(orders.router)
app.include_router(work_results.router)
# include data router
app.include_router(data_summary.router)
app.include_router(weather_router)


@app.get("/")
def read_root():
    return {"message": "MES Copilot API is running"}


unused_var = 10
