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
    return render_template('success.html')@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    if not db_collection:
        return jsonify({"status": "error", "message": "Database not connected"}), 500

    data = request.get_json()
    item_name = data.get('itemName')
    item_description = data.get('itemDescription')

    if not item_name or not item_description:
        return jsonify({"status": "error", "message": "Item Name and Item Description are required"}), 400

    try:
        todo_item = {
            "itemName": item_name,
            "itemDescription": item_description,
            "timestamp": datetime.now() # You'll need to import datetime
        }
        db_collection.insert_one(todo_item)
        return jsonify({"status": "success", "message": "To-Do item added successfully!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to add item: {str(e)}"}), 500




@app.route('/todo')
def todo_page():
    return render_template('todo.html')

if __name__ == '__main__':
    app.run(debug=True)
