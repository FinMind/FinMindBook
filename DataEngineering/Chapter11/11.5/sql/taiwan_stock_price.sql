CREATE TABLE `taiwan_stock_price` (
  `StockID` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `Transaction` bigint NOT NULL,
  `TradeVolume` int NOT NULL,
  `'TradeValue` bigint NOT NULL,
  `Open` float NOT NULL,
  `Max` float NOT NULL,
  `Min` float NOT NULL,
  `Close` float NOT NULL,
  `Change` float NOT NULL,
  `Date` date NOT NULL,
  PRIMARY KEY(`StockID`, `Date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci
PARTITION BY KEY (StockID)
PARTITIONS 10;