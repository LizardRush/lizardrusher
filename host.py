from flask import Flask, render_template, send_from_directory, abort
import requests
import json
from bs4 import BeautifulSoup

json_url = "https://raw.githubusercontent.com/LizardRush/lizardrusher/main/jsonFolder/websiteInfo.json"
response = requests.get(json_url)

if response.status_code == 200:
    website_info = response.json()
    social_media_links = website_info.get("external_links", {})
    if social_media_links:
        print("Social media links fetched successfully.")
    else:
        print("No social media links found in the JSON.")
else:
    print("Failed to fetch JSON data.")

# Fetch HTML content from the provided URL
html_url = "https://raw.githubusercontent.com/LizardRush/lizardrusher/main/htmlFolder/index.html"
html_response = requests.get(html_url)

if html_response.status_code == 200:
    soup = BeautifulSoup(html_response.content, 'html.parser')
    
    # Find the <nav> tag to insert social media links
    nav_tag = soup.find('nav')
    if nav_tag:
        ul_tag = nav_tag.find('ul')
        if ul_tag:
            links_tag = soup.new_tag('h3')
            links_tag.string = 'Links'
            ul_tag.insert_before(links_tag)
            
            # Insert social media links into the HTML content
            for platform, link in social_media_links.items():
                li_tag = soup.new_tag('li')
                a_tag = soup.new_tag('a', href=link)
                a_tag.string = platform.capitalize()
                li_tag.append(a_tag)
                ul_tag.append(li_tag)

            # Get the updated HTML content
            provided_html = soup.prettify()
        else:
            provided_html = "No <ul> tag found in the HTML content."
    else:
        provided_html = "No <nav> tag found in the HTML content."
else:
    provided_html = "Failed to fetch HTML content."

app = Flask(__name__)

@app.route('/')
def home():
    return provided_html

# Fetch HTML content from the URL
response = requests.get(html_url)

if response.status_code == 200:
    home_page_content = response.text
    if home_page_content:
        print("Home page content fetched successfully.")
    else:
        print("No content found in the HTML file.")
else:
    print("Failed to fetch HTML content.")

app = Flask(__name__)

# Route for the home page ('/')
@app.route('/')
def home():
    return home_page_content

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
