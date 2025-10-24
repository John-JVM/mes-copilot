import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from database import engine, Base
from routers import orders, work_results
from routers import data_summary
from routers.weather import router as weather_router
from middlewares.logging_middleware import LoggingMiddleware
from middlewares.jwt_middleware import JWTMiddleware

# 로깅 설정을 보다 유연하고 효율적으로 개선
# - LOG_LEVEL 환경변수로 레벨 제어 (기본 INFO)
# - debug 호출 시 비용 큰 계산이 필요한 경우를 대비한 helper 제공
# - f-string 대신 지연 포맷 (%s) 사용 권장 (logging 모듈이 필요 시점에만 포맷 수행)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

LOG_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO), format=LOG_FORMAT, datefmt=DATE_FORMAT)
logger = logging.getLogger("mes_copilot")

# 효율적인 debug 호출을 위한 helper
# 사용 예: debug("Expensive data size: %d", len(data))
# 내부에서 현재 레벨을 먼저 확인하므로 불필요한 연산을 피할 수 있음.
def debug(msg: str, *args, **kwargs):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(msg, *args, **kwargs)

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

# Add JWT middleware (필요 시 활성화)
# app.add_middleware(JWTMiddleware)

app.include_router(orders.router)
app.include_router(work_results.router)
# include data router
app.include_router(data_summary.router)
app.include_router(weather_router)

@app.get("/")
def read_root():
    debug("Root endpoint accessed")  # 예시 debug 호출 (지연 포맷 적용)
    return {"message": "MES Copilot API is running"}

unused_var = 10
