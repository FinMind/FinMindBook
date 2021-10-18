CREATE TABLE taiwan_stock_institutional_investors(
    `name` VARCHAR(20),
    `buy` BIGINT(64),
    `sell` BIGINT(64),
    `stock_id` VARCHAR(10),
    `date` DATE,
    PRIMARY KEY(`stock_id`, `date`, `name`)
) PARTITION BY KEY(`stock_id`) PARTITIONS 10;