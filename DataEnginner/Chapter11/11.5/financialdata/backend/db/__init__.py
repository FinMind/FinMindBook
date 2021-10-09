from financialdata.backend.db.router import (
    Router,
)
from financialdata.backend.db.db import *

router = Router()
mysql_database = MysqlDataBase()


def get_db_router():
    return router
