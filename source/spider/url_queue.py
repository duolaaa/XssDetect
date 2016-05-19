#_*_coding:utf-8_*_

import Queue
import re

from spider_url import SpiderUrl

class UrlQueue(object):
	"""
	url统一管理
	"""

	def __init__(self, root_url):
		# 待爬取的数据不限长度
		self.url_queue = Queue.Queue(maxsize = -1)
		# url过滤器
		self.url_filter = set()
		# 已爬取过的url
		self.old_urls = set()

		# 初始化
		self.url_queue.put(SpiderUrl(root_url, 0))
		self.domain = re.match(r"^(http(s)?://)?([\w-]+\.)+[\w-]+/?",root_url,re.M|re.I).group()

	def __add_new_url(self, spider_url):
		"""
		将连接添加到带爬取队列中并设置过滤器
		"""
		if (self.domain is None) or (spider_url is None):
			return

		url_str = spider_url.get_url()
		new_domain = re.match(r"^(http(s)?://)?([\w-]+\.)+[\w-]+/?",url_str,re.M|re.I)
		if url_str not in self.url_filter and new_domain and (new_domain.group()==self.domain):
			# 将url添加到带待爬取的url队列
			self.url_queue.put(spider_url)
			# 同时将url添加到过滤器
			self.url_filter.add(url_str)


	def put(self, urls_str, depth):
		"""
		批量添加新链接
		"""
		if urls_str is None or len(urls_str) == 0:
			return

		for url_str in urls_str:
			self.__add_new_url(SpiderUrl(url_str, depth))

	def is_empty(self):
		"""
		判断是否还有待爬取的链接
		"""
		return self.url_queue.empty()


	def get(self):
		# 获取带爬取的链接
		new_url = self.url_queue.get()
		# 将连接添加到已爬取的连接
		self.old_urls.add(new_url)
		return new_url


	def clear(self):
		"""
		重置爬虫设置
		"""
		# 清空待爬取链接列表
		while not(self.url_queue.empty()):
			self.url_queue.get()

		# 重置过滤器
		self.url_filter.clear()
		# 清空已爬取的url队列
		self.old_urls.clear()