"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)



# Nuevo endpoint: Registro
@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "data no encontrada"}), 400

    campos_requeridos= ["email", "password"]
    for campo in campos_requeridos: 
        if campo not in data:
            return jsonify({"msg": f"el campo '{campo}' es requerido"}), 400
        

    email_existente= User.query.filter_by(email=data["email"]).first()
    if email_existente:
        return jsonify({"msg": "Este email ya está registrado"}), 409    


    try:

        nuevo_usuario= User(
            email=data["email"],
            password=data["password"]
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({"msg": "Usuario registrado con éxito", 
                        "email": nuevo_usuario.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


 #Login modificar 
@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # crea token de acceso
    access_token = create_access_token(identity=user.id)
    return jsonify({
        "msg": "Login exitoso",
        "token": access_token,
        "user_id": user.id,
        "email": user.email
    }), 200


# Nuevo endpoint: Private (requiere JWT válido)modificar
@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    user_id = get_jwt_identity()      # obtiene el user.id desde el token
    user = User.query.get(user_id)
    return jsonify({"ok": True, "user": user.serialize()}), 200