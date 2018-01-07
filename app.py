from flask import Flask, url_for, render_template
from spider import Spider
app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/search/<username>')
def search(username):
    print(username)
    spider = Spider()
    spider.crawl(username)
    return render_template('detail.html')

if __name__ == '__main__':
    app.run(debug=True)