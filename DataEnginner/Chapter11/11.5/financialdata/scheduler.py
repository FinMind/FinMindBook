import time
import datetime

from apscheduler.schedulers.background import (
    BackgroundScheduler,
)
from financialdata.producer import (
    Update,
)
from loguru import logger
from financialdata.backend.db import (
    mysql_database,
)
from financialdata.utility.common import (
    get_today,
)


def sent_crawler_task(table: str):
    mysql_database.create_table(table)
    start_date = (
        mysql_database.get_max_date(
            table
        )
    )
    end_date = get_today()
    Update(
        table=table,
        start_date=start_date,
        end_date=end_date,
    )


def main():
    scheduler = BackgroundScheduler(
        timezone="Asia/Taipei"
    )
    # 與 crontab 類似，設定何時執行，有小時、分鐘、秒參數，* 星號代表任意時間點
    scheduler.add_job(
        id="sent_crawler_task",
        func=lambda: sent_crawler_task(
            table="taiwan_stock_price"
        ),
        trigger="cron",
        hour="15",
        minute="0",
        day_of_week="mon-fri",
    )
    logger.info("sent_crawler_task")
    scheduler.start()


if __name__ == "__main__":
    main()
    while True:
        time.sleep(600)
