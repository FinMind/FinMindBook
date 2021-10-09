sql = """
CREATE TABLE `taiwan_stock_info` (
  `industry_category` varchar(32) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `stock_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `stock_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` varchar(4) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '上市twse/上櫃tpex',
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
"""
