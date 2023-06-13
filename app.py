from flask import Flask, request, render_template
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

pt = pickle.load(open('pt.pkl', 'rb'))


@app.route('/')  # http://127.0.0.1:8000/ şeklinde erişilmesi için
def index():
    get_books=pt.columns
    return render_template("index.html",get_books=get_books)


@app.route('/', methods=['POST'])  # http://127.0.0.1:8000/ şeklinde erişilmesi için
def tahmin():
    get_books = pt.columns
    books = pd.read_csv("Books.csv")
    user_input = pt[request.form.get('kitap')]
    similar = pt.corrwith(user_input)
    corrls = pd.DataFrame(similar, columns=["Correlation"])
    corrls.dropna(inplace=True)
    rslt = corrls.sort_values('Correlation', ascending=False).head(5)
    rslt2 = rslt.index
    liste = []
    for i in rslt2:
        liste.append(str((books[books["Book-Title"] == i]["Image-URL-L"][0:1])).split()[1])
    rslt3 = zip(rslt2, liste)
    return render_template("index.html", rslt3=rslt3,get_books=get_books)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
