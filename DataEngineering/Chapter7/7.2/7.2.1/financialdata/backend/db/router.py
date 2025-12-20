from financialdata.backend.db import clients


class Router:
    def __init__(self):
        self._mysql_financialdata_engine = (
            clients.get_mysql_financialdata_engine()
        )

    @property
    def mysql_financialdata_engine(
        self,
    ):
        return (
            self._mysql_financialdata_engine
        )
