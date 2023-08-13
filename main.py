from flask import Flask, request, jsonify,render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/scrape', methods=['Post'])
def scrape():
    url = request.json('url')
    # print(url)
    classtoscrape = request.json('classname')
    print(classtoscrape)
    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(soup)
            # Extract the title from the parsed HTML
        title = soup.title.text if soup.title else "Title Not Found"
        print(title)
        elements_with_class = soup.find_all(class_='classtoscrape')
        a =[]
        extracted_text = [a.append(element) for element in elements_with_class]
        return jsonify({
            "Title":title,
            "Quotes":extracted_text
        }),200

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error fetching webpage: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    ## COMMENTED FOR PUSHING