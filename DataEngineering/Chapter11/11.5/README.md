# FinMindBook 11.5 - 上傳台股資料至 MySQL

upload_data2mysql.py 會下載 FinMind 釋出的 csv，建立對應 table 並寫入 MySQL，
作為 11.6 Redash 視覺化的資料來源。使用前請先修改 get_mysql_financialdata_engine 內的 IP。

## taiwan_stock_info
    make download-taiwan-stock-info

## taiwan_stock_price
    make download-taiwan-stock-price

## taiwan_stock_institutional_investors
    make download-taiwan-stock-institutional-investors

## taiwan_stock_margin_purchase_short_sale
    make download-taiwan-stock-margin-purchase-short_sale

## taiwan_stock_holding_shares_per
    make download-taiwan-stock-holding-shares-per
