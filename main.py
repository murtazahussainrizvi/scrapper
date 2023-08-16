from flask import Flask, request, jsonify,send_file,make_response
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

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
        #print(soup)
            # Extract the title from the parsed HTML
        title = soup.title.text if soup.title else "Title Not Found"
        print(title)
        scraped_data = []
        json_data={}
        # json_data = json.load(jsonObject)
        for i in values_array:
            elements = soup.find_all(class_=i)
            print("elements",elements)
            for element in elements:
                scraped_data.append(element.get_text())
            json_data[i] = scraped_data
            scraped_data=[]
            # return_json = jsonify({i:json_data})
        # Replace with appropriate selector for your target table
        df = pd.DataFrame(json_data)
        excel_writer = pd.ExcelWriter('quotes.xlsx', engine='openpyxl')
        df.to_excel(excel_writer, sheet_name='Quotes', index=False)
        excel_writer.close()
        response = make_response(send_file('quotes.xlsx', as_attachment=True, download_name='quotes.xlsx'))
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        return response
        # return json_data, 200
        

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error fetching webpage: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    ## COMMENTED FOR PUSHING