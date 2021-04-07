CREATE TABLE `FinancialData`.`TaiwanStockPrice`(
    `StockID` VARCHAR(10) NOT NULL,
    `TradeVolume` INT NOT NULL,
    `Transaction` INT NOT NULL,
    `TradeValue` INT NOT NULL,
    `Open` FLOAT NOT NULL,
    `Max` FLOAT NOT NULL,
    `Min` FLOAT NOT NULL,
    `Close` FLOAT NOT NULL,
    `Change` FLOAT NOT NULL,
    `Date` DATE NOT NULL,
    PRIMARY KEY(`StockID`, `Date`)
)
