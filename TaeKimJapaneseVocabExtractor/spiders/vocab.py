import scrapy

class VocabSpider(scrapy.Spider):
    name = "vocab"
    allowed_domains = [ "http://www.guidetojapanese.org" ]
    start_urls = [
        "http://www.guidetojapanese.org/learn/grammar/writing",
    ]

    def parse(self, response):

        # grab vocab words
        for vocab in response.css('li').re(r'(?P<vocab>[\u3000-\u9faf]+)\s【(?P<reading>.*?)】 – (?P<translation>[\u0000-\u00ff]*)'):
            # get the vocab components
            term, reading, definition = vocab
            
            yield {
                "term" : term,
                "reading" : reading,
                "definition" : definition
            }

        # go to the next page, if it exists
        next_page = response.css('span.series-nav-right a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
