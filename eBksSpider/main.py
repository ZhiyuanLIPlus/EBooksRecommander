from scrapy import cmdline

#cmdline.execute("scrapy crawl ysXpathTest".split())
cmdline.execute("scrapy crawl ysXpathTest -o test.json".split())