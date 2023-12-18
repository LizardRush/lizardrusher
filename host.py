from flask import Flask, render_template, send_from_directory, abort
import requests
import json

app = Flask(__name__)

# URL for the JSON file containing pages and their raw links
pages_url = "https://raw.githubusercontent.com/LizardRush/lizardrusher/main/jsonFolder/websitePages.json"

# Fetch the page links from the JSON file
def fetch_page_links():
    try:
        response = requests.get(pages_url)
        if response.status_code == 200:
            return response.json()
        else:
            return {}
    except Exception as e:
        print("Error fetching page links:", e)
        return {}

# Load page links from the fetched JSON content
pages = fetch_page_links()

# Dictionary for all in-code errors
error_types = {
    1: "JSON error: Could not read URL",
    2: "Did not find error"
    3: "Error fetching website information from GitHub"
}

# URL to fetch JSON data
website_info_url = "https://raw.githubusercontent.com/LizardRush/lizardrusher/main/jsonFolder/websiteInfo.json"

def get_error(error):
    # Check if the error type exists in the dictionary, else return default error
    return error_types.get(error, error_types[2])

 Function to fetch the JSON data from GitHub
def fetch_website_info():
    url = "https://raw.githubusercontent.com/LizardRush/lizardrusher/main/jsonFolder/websiteInfo.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print("Error fetching website info:", e)
        return None

@app.route('/')
def index():
    # Fetch website information from GitHub
    website_info = fetch_website_info()

    if website_info:
        # Pass external links from website_info to the HTML template
        external_links = website_info.get("external_links", {})
        return render_template('index.html', external_links=external_links)
    else:
        # Handle if fetching data from GitHub fails
        return get_error(3)
@app.route('/home')
def index():
    try:
        # Fetch the JSON data from the URL
        response = requests.get(website_info_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Convert the response content to JSON
            website_info = response.json()
            # Return JSON data or pass it to the template for rendering
            return render_template('index.html', website_info=website_info)
        else:
            # Handle error and display an error message
            error_message = get_error(1)
            return f"Error: {error_message}"
    except Exception as e:
        # Handle any other exceptions and display an error message
        error_message = get_error(2)
        return f"Error: {error_message}"

# Route to serve static files (like CSS, JS, images, etc.)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Route to serve different pages based on the requested route
@app.route('/<page>')
def serve_page(page):
    if page in pages:
        # Fetch the raw link of the requested page from the fetched page links
        raw_link = pages[page]
        # Fetch the content of the page from the raw link and return it
        page_content = requests.get(raw_link).text
        return page_content
    else:
        # If the requested page doesn't exist, return a 404 error
        return abort(404)

if __name__ == '__main__':
    app.run(debug=True)
