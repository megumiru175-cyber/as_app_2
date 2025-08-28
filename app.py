from flask import Flask,render_template
from  ebaysoldgazo import get_ebay_items


app = Flask(__name__)

@app.route('/')
def index():
    books =get_ebay_items()
    return render_template('index.html',books=books)
if  __name__ == '__main__':
    app.run(debug=True)
