from pymongo import MongoClient

# Connect to your MongoDB server
client = MongoClient("mongodb+srv://okoride0:lindahst1@database1.a17zh8w.mongodb.net/?retryWrites=true&w=majority")

# Select the appropriate database and collection
db = client["database1"]
collection = db["jijiProducts"]

# Add the "source" field to all documents
collection.update_many({}, {"$set": {"source": "From jiji"}})

# Close the MongoDB connection
client.close()
