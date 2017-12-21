from flask import Flask, url_for
app = Flask(__name__)

@app.route('/index')
def login():
    pass

@app.route('/search/<username>')
def search(username):
    pass

if __name__ == '__main__':
    app.run(debug=True)