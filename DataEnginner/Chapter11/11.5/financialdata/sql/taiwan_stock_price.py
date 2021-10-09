sql = """
CREATE TABLE `taiwan_stock_price` (
  `stock_id` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `Trading_turnover` bigint NOT NULL,
  `Trading_Volume` int NOT NULL,
  `Trading_money` bigint NOT NULL,
  `open` float NOT NULL,
  `max` float NOT NULL,
  `min` float NOT NULL,
  `close` float NOT NULL,
  `spread` float NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci
PARTITION BY KEY (stock_id)
PARTITIONS 10;
"""
