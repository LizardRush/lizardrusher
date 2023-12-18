from flask import Flask

app = Flask(__name__)

@app.route('/', subdomain='lizrusher')
def index():
    return 'Welcome to LizRusher! This is your homepage.'

if __name__ == '__main__':
    app.run(debug=True)

