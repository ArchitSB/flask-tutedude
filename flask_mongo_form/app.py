from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

#Enter your URI
MONGO_URI = "mongodb+srv:/?retryWrites=true&w=majority&appName=MyLearningBackend"
client = MongoClient(MONGO_URI)
db = client['formDB']
collection = db['submissions']

@app.route('/', methods=['GET', 'POST'])
def form():
    error = None
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            if not name or not email:
                raise Exception("Name and Email are required")
            collection.insert_one({"name": name, "email": email})
            return redirect(url_for('success'))
        except Exception as e:
            error = str(e)
    return render_template('form.html', error=error)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
