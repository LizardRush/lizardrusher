from flask import Flask
import requests
# dictionary for all in code errors
error_types= {
    1: "JSON error, could not read url",
    2: "Did not find error"
}
url = "https://raw.githubusercontent.com/LizardRush/lizardrusher/main/jsonFolder/websiteInfo.json"
def get_error(error):
    if error_types[error]:
        rerurn error_types[error]
    else
        return error_types[2]
if response.status_code == 200:
    website_info = response.json()
else:
    print(get_error(1))
# Fetch the JSON data from the URL
response = requests.get(url)

app = Flask(__name__)

@app.route('/', subdomain=)
def index():
    return 'Welcome to LizRusher! This is your homepage.'

if __name__ == '__main__':
    app.run(debug=True)

