from sqlalchemy.exc import IntegrityError
from app.models.proveedor import Proveedor
from datetime import datetime
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller

class ProveedorController(Controller):

    @staticmethod
    def get_all() -> tuple[Response, int]:
        proveedor_list = db.session.execute(db.select(Proveedor).order_by(db.desc(Proveedor.id))).scalars().all()
        if len( proveedor_list) >0:
            proveedores_to_dict = [proveedor.to_dict() for proveedor in proveedor_list ]
            return jsonify(proveedores_to_dict), 200 
        return jsonify({"message": 'datos no encontrados'}), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
        if proveedor:
            return jsonify(proveedor.to_dict()), 200
        return jsonify({"message": 'proveedor no encontrado'}), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        nombre = request.get('nombre')
        contacto = request.get('contacto')
        telefono = request.get('telefono')
        email = request.get('email')
        
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if contacto is None:
            error = 'El contacto es requerido'
        if telefono is None:
            error = 'El telefono es requerido'
        if email is None:
            error = 'El email es requerido'
        
            
        if error is None:
            try:
                proveedor = Proveedor(nombre=nombre, 
                                    contacto=contacto,
                                    telefono=telefono,
                                    email=email)
                db.session.add(proveedor)
                db.session.commit()
                return jsonify({'message': "proveedor creado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "proveedor ya registrado"}), 409
        return jsonify ({'message': error}), 422
    
    @staticmethod
    def update(request, id)->tuple[Response, int]:
        nombre= request.get('nombre')
        contacto= request.get('contacto')
        telefono = request.get('telefono')
        email = request.get('email')

        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if contacto is None:
            error = 'El contacto es requerido'
        if telefono is None:
            error = 'El telefono es requerido'
        if email is None:
            error = 'El email es requerido'
            
        if error is None:
            proveedor = db.session.get(Proveedor, id)
            if proveedor:
                try:
                    proveedor.nombre = nombre
                    proveedor.contacto = contacto
                    proveedor.telefono = telefono
                    proveedor.email = email
                    proveedor.updated_at = datetime.now()
                    db.session.commit()
                    return jsonify({'message':'proveedor modificado con exito'}), 200
                except IntegrityError:
                    error = 'El proveedor no se pudo actualizar, algo fallo.' 
                    return jsonify({'message':error}), 409
            else:     
                error = 'proveedor no encontrado'
            
        return jsonify({'message':error}), 404
    
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
        error = None
        if proveedor:
            db.session.delete(proveedor)
            db.session.commit()
            return jsonify({'message':'El proveedor fue eliminado con exito'}), 200
        else:
            error = 'proveedor no encontrado'
        return jsonify({'message':error}), 404