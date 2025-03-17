from loguru import logger
from datetime import datetime
from pytz import timezone


logger.add(
    f"logs/{datetime.now(timezone('Europe/Moscow')).strftime('%d-%m-%Y')}.log",
    format="{time} {level} {message}\n",
    rotation="500MB",
    level="INFO",
    enqueue=True,
)
