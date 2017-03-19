# EBooksRecommander
An online Fiction Recommandation Project
A pratical project is to build a accurate recommandation algo to recommand online fictions by using the collaborative filtering algo.
* eBksSpider:
  * Scrapy code to scrapy data from [Yousuu](www.yousuu.com/booklist)
* eBksRecommder:
  * dataloader.py to process the data into a dict
  * func.py include the functions to calculate the similarity (**Euclidean Distance** and **Pearson correlation**) and do the recommandation