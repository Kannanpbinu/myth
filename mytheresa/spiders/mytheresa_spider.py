import scrapy

class MytheresaSpiderSpider(scrapy.Spider):
    name = "mytheresa_spider"
    allowed_domains = ["www.mytheresa.com"]
    start_urls = ["https://www.mytheresa.com/int/en/men/shoes?rdr=mag"]
    
    # Counter to track the number of pages scraped
    page_counter = 0
    max_pages = 1000  # Limit to 1000 pages

    def parse(self, response):
        # Extract product links from the current page
        product_links = response.xpath('//a[contains(@class, "item__link")]/@href').getall()

        for product_link in product_links:
            yield response.follow(product_link, callback=self.parse_product)

        # Find the link to the next page
        next_page = response.xpath('//a[contains(@class, "pagination_item_text--next")]/@href').get()

        # If the next page exists and we haven't scraped 1000 pages yet, follow the link
        if next_page and self.page_counter < self.max_pages:
            self.page_counter += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        # Extract product details
        product_name = response.xpath('//h1[@class="product_areabranding_name"]/text()').extract()
        product_brand = response.xpath('//a[@class="product_areabrandingdesigner_link"]/text()').extract()
        product_breadcrumbs = response.xpath('//ol[@class="breadcrumb"]//li//text()').extract()
        product_listing_price = response.xpath('//span[contains(@class, "pricing_pricesvalue--original")]/span[@class="pricingprices_price"]/text()').extract()
        product_offer_price = response.xpath('//span[contains(@class, "pricing_pricesvalue--discount")]/span[@class="pricingprices_price"]/text()').extract()
        product_discount = response.xpath('//span[@class="pricing_info_percentage"]/text()').extract()
        product_image_url = response.xpath('//img[@class="zoompro"]/@src').extract()
        product_id = response.xpath('//li[contains(text(), "Item No.")]/text()').extract()
        product_size = response.xpath('//div[@class="dropdown_select_content"]//span/text()').extract()
        product_description = response.xpath('//div[@class="productinfo_block"]//ul[@class="accordionbody_content"]//li/text()').extract()

        # Yield the extracted data for each product
        yield {
            'name': product_name,
            'brand': product_brand,
            'breadcrumbs': product_breadcrumbs,
            'listing_price': product_listing_price,
            'offer_price': product_offer_price,
            'discount': product_discount,
            'image': product_image_url,
            'id': product_id,
            'size': product_size,
            'description': product_description,
            'url': response.url,
        }
