"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200


@app.route('/member/', methods=['POST'])
def add_member():
    new_member = request.json
    print(new_member)
    jackson_family.add_member(new_member)
    return jsonify({"done":"usuario creado"}), 200

#recuperar solo un miembro de la familia
@app.route('/members/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    member_found = jackson_family.get_member(member_id)
    if not member_found:
        return jsonify({"err_msg": "member not found"}), 400
    else:
        return jsonify(member_found), 200
    
    
#elimina un miembro de la famlia
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_family_member(member_id):
    eliminar_familiar = jackson_family.delete_member(member_id)
    if not eliminar_familiar:
        return jsonify({"msg": "familiar no encontrado"}), 400
    
    return jsonify("familiar borrado"), 200

#actualizar miembro de la familia
@app.route('/member/<int:member_id>', methods=['PUT'])
def update_family_member(member_id):
    new_member = request.json
    updated_member = jackson_family.update_member(member_id, new_member)
    if not updated_member:
        return jsonify({"msg": "member not found"}), 400
    return jsonify("done")

    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

