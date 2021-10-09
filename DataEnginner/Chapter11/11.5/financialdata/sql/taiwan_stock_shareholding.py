sql = """
CREATE TABLE `taiwan_stock_shareholding` (
  `stock_id` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `stock_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `NumberOfSharesIssued` float DEFAULT NULL COMMENT '外資尚可投資股數',
  `ForeignInvestmentRemainingShares` float DEFAULT NULL COMMENT '外資尚可投資股數',
  `ForeignInvestmentShares` float DEFAULT NULL COMMENT '外資持有股數',
  `ForeignInvestmentRemainRatio` float DEFAULT NULL COMMENT '外資尚可投資比例',
  `ForeignInvestmentSharesRatio` float DEFAULT NULL COMMENT '外資持股比例',
  `ForeignInvestmentUpperLimitRatio` float DEFAULT NULL COMMENT '外資投資上限',
  `ChineseInvestmentUpperLimitRatio` float DEFAULT NULL COMMENT '陸資投資上限',
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci
PARTITION BY KEY (stock_id)
PARTITIONS 10;
"""
