sql = """
CREATE TABLE taiwan_stock_holding_shares_per (
    `HoldingSharesLevel` VARCHAR(19),
    `people` INT(10),
    `unit` BIGINT(64),
    `percent` FLOAT,
    `stock_id` VARCHAR(10),
    `date` DATE,
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`stock_id`,`date`,`HoldingSharesLevel`)
)
PARTITION BY KEY(stock_id)
PARTITIONS 10;
"""
