from tasks import crawler
 
# 發送任務有兩種方式
# 1.
crawler.delay(x=0)
# 2.
# task = crawler.s(x=0)
# task.apply_async()
