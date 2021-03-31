import os

MYSQL_MONITOR_HOST = os.environ.get("MYSQL_MONITOR_HOST", "127.0.0.1")
MYSQL_MONITOR_USER = os.environ.get("MYSQL_MONITOR_USER", "root")
MYSQL_MONITOR_PASSWORD = os.environ.get("MYSQL_MONITOR_PASSWORD", "test")
MYSQL_MONITOR_PORT = int(os.environ.get("MYSQL_MONITOR_PORT", "3306"))
MYSQL_MONITOR_DATABASE = os.environ.get("MYSQL_MONITOR_DATABASE", "Monitor")

MYSQL_DATA_HOST = os.environ.get("MYSQL_DATA_HOST", "127.0.0.1")
MYSQL_DATA_USER = os.environ.get("MYSQL_DATA_USER", "root")
MYSQL_DATA_PASSWORD = os.environ.get("MYSQL_DATA_PASSWORD", "test")
MYSQL_DATA_PORT = int(os.environ.get("MYSQL_DATA_PORT", "3306"))
MYSQL_DATA_DATABASE = os.environ.get("MYSQL_DATA_DATABASE", "FinancialData")
