# Importing Path to save data in files
from pathlib import Path, PurePath
# Importing scrapy
import scrapy

# Create the directory if it doesn't exist
directory_path = Path("pages")
directory_path.mkdir(parents=True, exist_ok=True)


# Creating class of the spider
class webCrawler(scrapy.Spider):
    # Giving a name to the spider
    name = "webExplorer"

    # Creatng method to start the crawling and scrapying
    def start_requests(self):
        # Seed URLs 
        urls = "https://quotes.toscrape.com/page/"
        # Requesing the URLs
        for page in range(10):
            url = f"{urls}{page + 1}"
            yield scrapy.Request(url = url, callback = self.parse)

    # Method parse function 
    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

    # Method to parse the information of each visited link
    def parse1(self, response):
        # Getting the number of the page
        page = response.url.split("/")[-2]

        filename = f"quotes-{page}.html"

        # Now proceed to create and write to the file
        file_path = directory_path / filename

        # Creating a file with the filemane and saving the body of the response there
        file_path.write_bytes(response.body)

        # Loging the succesful save
        self.log(f"Saved file {filename}")