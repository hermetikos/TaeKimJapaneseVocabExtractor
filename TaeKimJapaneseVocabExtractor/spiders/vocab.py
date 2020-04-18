import scrapy
from scrapy.shell import inspect_response
import re

class VocabSpider(scrapy.Spider):
	i = 1
	name = "vocab"
	allowed_domains = [ "guidetojapanese.org" ]
	start_urls = [
		"http://www.guidetojapanese.org/learn/grammar/stateofbeing",
		"http://www.guidetojapanese.org/learn/grammar/essential",
		"http://www.guidetojapanese.org/learn/grammar/specialexpressions",
		"http://www.guidetojapanese.org/learn/grammar/advanced"
	]

	def parse(self, response):
		# grab vocab words
		for text in response.css('ol li::text').getall():
			# r'(?P<vocab>[\u3000-\u9faf]+)\s【(?P<reading>.*?)】 – (?P<translation>[\u0000-\u00ff]*)'
			# get the vocab components

			vocab = re.search(r'(?P<term>[\u3000-\u9faf]+)\s【(?P<reading>.*?)】 – (?P<translation>[\u0000-\u00ff]*)', text)

			if vocab:
				term = vocab.group("term")
				reading = vocab.group("reading").replace("・","")
				translation = vocab.group("translation")
				title = response.css('h1.entry-title::text').get()

				yield {
					"term" : term,
					"reading" : reading,
					"translation" : translation,
					"section" : title
				}
		
		# go to the next page, if it exists
		next_page = response.css('span.series-nav-right a::attr(href)').get()
		if next_page is not None:
			yield response.follow(next_page, callback=self.parse)
