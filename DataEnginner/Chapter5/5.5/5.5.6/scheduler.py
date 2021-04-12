import time

from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger


def sent_crawler_task(dataset: str):
    logger.info(f"sent_crawler_task {dataset}")


def main():
    scheduler = BackgroundScheduler(timezone="Asia/Taipei")
    scheduler.add_job(
        id="sent_crawler_task",
        func=sent_crawler_task,
        trigger="cron",
        hour="*",
        minute="0",
        day_of_week="*",
        second="*/5",
        args=["taiwan_stock_price"],
    )
    logger.info("sent_crawler_task")
    scheduler.start()


if __name__ == "__main__":
    main()
    while True:
        time.sleep(600)
