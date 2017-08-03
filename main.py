from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 启动爬虫项目
execute(["scrapy","crawl","jobbole"])