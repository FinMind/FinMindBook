SELECT if(tsii.buy-tsii.sell>0, tsii.buy-tsii.sell,0) AS '買超',
       if(tsii.sell-tsii.buy>0, tsii.sell-tsii.buy,0) AS '賣超',
       stock_price.Close AS '股價',
       tsii.date AS date
FROM taiwan_stock_institutional_investors AS tsii
INNER JOIN taiwan_stock_info AS si ON si.stock_id = tsii.stock_id
INNER JOIN taiwan_stock_price AS stock_price ON tsii.stock_id = stock_price.StockID
AND tsii.date = stock_price.Date
WHERE tsii.name = 'Foreign_Investor'
  AND si.stock_name = '台積電'
  AND tsii.date >= '2015-01-01'