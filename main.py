from flask import Flask, request, jsonify,send_file,make_response
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['POST'])
def scrape():
    requestJsonObject = request.json
    print("jsonobject ==>",requestJsonObject)
    url= requestJsonObject.get("url")
    baseurl = url
    classtoextract = requestJsonObject.get("class")
    nextpagetoextract = requestJsonObject.get("nextpage")
    print(nextpagetoextract, "-----murtaza kutiya")
    values_array = classtoextract.split(',')
    print("values array=",values_array)
    if not url:   
        return jsonify({'error': 'Missing URL parameter'}), 400
    try:
        json_data={"data":[

        ]}
        while url:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            #print(soup)
                    # Extract the title from the parsed HTML
            title = soup.title.text if soup.title else "Title Not Found"
            print(title)
            scraped_data = []
        
                # json_data = json.load(jsonObject)
            for i in values_array:
                elements = soup.find_all(class_=i)
                print("elements",elements)
                for element in elements:
                    scraped_data.append(element.get_text())
                json_data["data"].append(scraped_data)
                scraped_data=[]
            try:
                next_page_link = soup.find("li", class_=nextpagetoextract).find("a")["href"]
                next_page_url = baseurl + next_page_link
                print("=====>",next_page_link,next_page_url)
                if next_page_url==url:
                    break
                url = next_page_url
            except:
                print('The scraper has gone through all the pages')
                break
         # return_json = jsonify({i:json_data})
        # Replace with appropriate selector for your target table
        # Extract quotes and authors from the alternating data
        quotes = json_data["data"][::2]  # Extract even-indexed elements
        authors = json_data["data"][1::2]  # Extract odd-indexed elements

        # Create a DataFrame
        df = pd.DataFrame({"Quote": quotes, "Author": authors})
        # Create a new DataFrame to hold the separated data
        exploded_df = df.explode(['Quote', 'Author'], ignore_index=True)

        excel_writer = pd.ExcelWriter('quotes.xlsx', engine='openpyxl')
        exploded_df.to_excel(excel_writer, sheet_name='Quotes', index=False)
        excel_writer.close()
        response = make_response(send_file('quotes.xlsx', as_attachment=True, download_name='quotes.xlsx'))
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        return response
    # return json_data, 
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error fetching webpage: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
