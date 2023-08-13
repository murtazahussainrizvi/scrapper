# app.py

from flask import Flask, request, jsonify
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from generic_spider import GenericSpider

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        url = data.get('url')
        columns = data.get('columns')

        if not url or not columns:
            return jsonify({'error': 'Invalid input data'}), 400

        process = CrawlerProcess(get_project_settings())
        process.crawl(GenericSpider, url=url, columns=columns)
        process.start()

        return jsonify({'message': 'Scraping completed successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)