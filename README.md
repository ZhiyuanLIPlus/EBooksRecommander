# EBooksRecommander
网络小说推荐系统实战

因为个人看网络小说经常出现书荒的情况，就想使用协同过滤推荐算法为自己打造一个网络小说推荐工具。
* eBksSpider:
  * 抓取 [优书网](http://www.yousuu.com/booklist) 所有书单的爬虫代码
* eBksRecommder:
  * dataloader.py 清洗抓取数据，将抓取数据以{用户：{书名：评分}}的字典形式存储
  * func.py 算法实现部分
    *  读取UserPrefs.txt中用户喜好书单以及书评
	*  使用不同度量方法(**欧氏距离**，**皮尔逊相似性**和**Tanimoto系数**)为每本小说计算前10最相似小说
	*  实施协同过滤算法
	
# EBooksRecommander  
An online Fiction Recommandation Project

The objective is to build an accurate recommandation algo to recommand online fictions by using the collaborative filtering algo.
* eBksSpider:
  * Scrapy code to scrapy data from [Yousuu](http://www.yousuu.com/booklist)
* eBksRecommder:
  * dataloader.py to process the data into a dict
  * func.py include the functions to calculate the similarity (**Euclidean Distance**，**Pearson Correlation** and **Tanimoto Coefficient**) and do the recommandation