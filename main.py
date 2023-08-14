from flask import Flask, request, jsonify,render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    requestJsonObject = request.json
    print("jsonobject ==>",requestJsonObject)
    url= requestJsonObject.get("url")
    classtoextract = requestJsonObject.get("class")
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
        scraped_data = []
        elements = soup.find_all(class_=classtoextract)
        for element in elements:
            scraped_data.append(element.get_text())
        # Replace with appropriate selector for your target table
        return jsonify({
            "Title":title,
            'Quotes': scraped_data

        }),200

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error fetching webpage: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    ## COMMENTED FOR PUSHING