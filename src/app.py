from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/bd_alimentos'

mongo = PyMongo(app)

# Save data into db
@app.route('/foods', methods=['POST'])
def create_food():
  # Receiving data
  name = request.json['name']
  protein = request.json['protein']
  calorie = request.json['calorie']
  if name and protein and calorie:
    id = mongo.db.foods.insert_one({
        'name': name,
        'protein': protein,
        'calorie': calorie
      })
    response = {
        'id': str(id),
        'name': name,
        'protein': protein,
        'calorie': calorie
      }
    return response
  else:
    return not_found()

# List data from db
@app.route('/foods', methods=['GET'])
def get_foods():
  foods = mongo.db.foods.find()
  response = json_util.dumps(foods)
  return Response(response, mimetype='application/json')

# Return data from foods by id
@app.route('/foods/<id>', methods=['GET'])
def get_food(id):
  food = mongo.db.foods.find_one({'_id': ObjectId(id)})
  if food:
    response = json_util.dumps(food)
    return Response(response, mimetype='application/json')
  else:
    return not_found()
  
# Delete data from foods by id
@app.route('/foods/<id>', methods=['DELETE'])
def delete_food(id):
  mongo.db.foods.delete_one({'_id': ObjectId(id)})
  response = jsonify({'message': 'Food ' + id + ' was deleted successfully'})
  return response

# Update data from foods by id
@app.route('/foods/<id>', methods=['PUT'])
def update_food(id):
  name = request.json['name']
  protein = request.json['protein']
  calorie = request.json['calorie']
  if name and protein and calorie:
    mongo.db.foods.update_one({'_id': ObjectId(id)}, {"$set": {
        'name': name,
        'protein': protein,
        'calorie': calorie
      }})
    response = jsonify({'message': 'Food ' + id + ' was update succesfully'})
    return response
  else:
    return not_found()

# Return not data template
@app.errorhandler(404)
def not_found(error=None):
  response = jsonify({
      'message': 'Resource not found: ' + request.url,
      'status': 404
    })
  response.status_code = 404
  return response

if __name__ == "__main__":
  app.run(debug=True)
