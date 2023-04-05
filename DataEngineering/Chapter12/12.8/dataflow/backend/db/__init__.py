from dataflow.backend.db.router import (
    Router,
)
from dataflow.backend.db.db import *

router = Router()


def get_db_router():
    return router
