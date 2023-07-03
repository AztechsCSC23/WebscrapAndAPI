#!/home/okori/pythonproject/unicart_env/bin/python

from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://okoride0:lindahst1@database1.a17zh8w.mongodb.net/?retryWrites=true&w=majority")

@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('query')
    
    # Connect to the MongoDB collection
    db = client['scraped_data']
    collection = db['products']
    
    # Search the collection for matching products
    matching_products = collection.find({'name': {'$regex': query, '$options': 'i'}})
    
    # Prepare the response
    results = []
    for product in matching_products:
        results.append({
            'source': product['source'],
            'name': product['name'],
            'price': product['price'],
            'product_rating': product['rating']
        })
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

