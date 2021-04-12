from financialdata.backend.db.router import Router
from financialdata.backend.db.db import *

router = Router()


def get_db_router():
    return router
