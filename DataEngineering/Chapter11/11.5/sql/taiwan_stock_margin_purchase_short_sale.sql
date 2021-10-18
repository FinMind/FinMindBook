CREATE TABLE `FinancialData`.`taiwan_stock_margin_purchase_short_sale`(
    `stock_id` VARCHAR(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '股票代碼',
    `MarginPurchaseBuy` BIGINT NOT NULL COMMENT '融資買進',
    `MarginPurchaseSell` BIGINT NOT NULL COMMENT '融資賣出',
    `MarginPurchaseCashRepayment` BIGINT NOT NULL COMMENT '融資現金償還',
    `MarginPurchaseYesterdayBalance` BIGINT NOT NULL COMMENT '融資昨日餘額',
    `MarginPurchaseTodayBalance` BIGINT NOT NULL COMMENT '融資今日餘額',
    `MarginPurchaseLimit` BIGINT NOT NULL COMMENT '融資限額',
    `ShortSaleBuy` BIGINT NOT NULL COMMENT '融券買進',
    `ShortSaleSell` BIGINT NOT NULL COMMENT '融券賣出',
    `ShortSaleCashRepayment` BIGINT NOT NULL COMMENT '融券償還',
    `ShortSaleYesterdayBalance` BIGINT NOT NULL COMMENT '融券昨日餘額',
    `ShortSaleTodayBalance` BIGINT NOT NULL COMMENT '融券今日餘額',
    `ShortSaleLimit` BIGINT NOT NULL COMMENT '融券限制',
    `OffsetLoanAndShort` BIGINT DEFAULT NULL COMMENT '資券互抵',
    `date` DATE NOT NULL COMMENT '日期',
    PRIMARY KEY(`stock_id`, `date`)
) PARTITION BY KEY(`stock_id`) PARTITIONS 10;