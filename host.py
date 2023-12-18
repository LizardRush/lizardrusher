from flask import Flask, render_template, send_from_directory, abort
import requests
import json

# Fetch JSON data from the URL containing page names and their respective URLs
json_url = "https://raw.githubusercontent.com/LizardRush/lizardrusher/main/jsonFolder/websitePages.json"
response = requests.get(json_url)

if response.status_code == 200:
    pages_data = response.json()
    pages = pages_data  # Assuming the JSON structure directly contains page data as a dictionary
    if pages:
        print("Pages data fetched successfully.")
    else:
        print("No page data found in the JSON.")
else:
    print("Failed to fetch JSON data.")

app = Flask(__name__)

# Define a separate handler for the "home" page
def home_handler():
    page_content = requests.get(pages['home']).text
    return page_content

app.add_url_rule('/', endpoint='home', view_func=home_handler)

# Iterate through the pages dictionary and create routes dynamically
for page, page_url in pages.items():
    if page != 'home':  # Skip 'home' page as it's already added
        route_path = f'/{page}'
        
        def generate_handler(url):
            def handler():
                page_content = requests.get(url).text
                return page_content
            return handler

        app.add_url_rule(route_path, endpoint=page, view_func=generate_handler(page_url))

if __name__ == '__main__':
    app.run(debug=True)
