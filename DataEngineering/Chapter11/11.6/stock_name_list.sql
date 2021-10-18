SELECT DISTINCT
    `stock_name`
FROM
    `taiwan_stock_info`
WHERE
    (
        `industry_category` NOT IN(
            '認購權證(不含牛證)',
            '可展延牛證',
            '認售權證(不含熊證)',
            '熊證(不含可展延熊證)',
            '牛證(不含可展延牛證)',
            '不動產投資信託證券',
            '上櫃指數股票型基金(ETF)',
            '受益證券',
            '指數投資證券(ETN)',
            'ETN',
            '存託憑證',
            '封閉式基金'
        )
    )