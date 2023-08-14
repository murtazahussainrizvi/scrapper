from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    requestJsonObject = request.json
    print("jsonobject ==>",requestJsonObject)
    url= requestJsonObject.get("url")
    classtoextract = requestJsonObject.get("class")
    values_array = classtoextract.split(',')
    print("values array=",values_array)
    if not url:   
        return jsonify({'error': 'Missing URL parameter'}), 400
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        print("soup==>",soup)
        scraped_data = []
        for i in values_array:
            elements = soup.find_all(class_=i)
            for element in elements:
                scraped_data.append(element.get_text())
            return_json = jsonify({i:scraped_data})
        # Replace with appropriate selector for your target table
        return return_json, 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error fetching webpage: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    ## COMMENTED FOR PUSHING