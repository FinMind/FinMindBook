CREATE TABLE `financialdata`.`TaiwanStockPrice`(
    `StockID` VARCHAR(10) NOT NULL,
    `TradeVolume` BIGINT NOT NULL,
    `Transaction` INT NOT NULL,
    `TradeValue` BIGINT NOT NULL,
    `Open` FLOAT NOT NULL,
    `Max` FLOAT NOT NULL,
    `Min` FLOAT NOT NULL,
    `Close` FLOAT NOT NULL,
    `Change` FLOAT NOT NULL,
    `Date` DATE NOT NULL,
    PRIMARY KEY(`StockID`, `Date`)
);

CREATE TABLE `financialdata`.`TaiwanFuturesDaily`(
    `Date` DATE NOT NULL,
    `FuturesID` VARCHAR(10) NOT NULL,
    `ContractDate` VARCHAR(30) NOT NULL,
    `Open` FLOAT NOT NULL,
    `Max` FLOAT NOT NULL,
    `Min` FLOAT NOT NULL,
    `Close` FLOAT NOT NULL,
    `Change` FLOAT NOT NULL,
    `ChangePer` FLOAT NOT NULL,
    `Volume` FLOAT NOT NULL,
    `SettlementPrice` FLOAT NOT NULL,
    `OpenInterest` INT NOT NULL,
    `TradingSession` VARCHAR(11) NOT NULL,
    PRIMARY KEY(`FuturesID`, `Date`)
)

