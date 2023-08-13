from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        scraped_data = []

        # Replace with appropriate selector for your target table
        table = soup.find('table')
        if table:
            for row in table.find_all('tr'):
                row_data = [cell.get_text() for cell in row.find_all('td')]
                scraped_data.append(row_data)

            return jsonify({'data': scraped_data}), 200
        else:
            return jsonify({'error': 'Table not found in the webpage'}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error fetching webpage: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)