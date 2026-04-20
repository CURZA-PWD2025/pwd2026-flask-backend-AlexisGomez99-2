from sqlalchemy.exc import IntegrityError
from app.models.categoria import Categoria
from datetime import datetime
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller

class CategoriaController(Controller):

    @staticmethod
    def get_all() -> tuple[Response, int]:
        categorias_list = db.session.execute(db.select(Categoria).order_by(db.desc(Categoria.id))).scalars().all()
        if len( categorias_list) >0:
            categorias_to_dict = [categoria.to_dict() for categoria in categorias_list ]
            return jsonify(categorias_to_dict), 200 
        return jsonify({"message": 'datos no encontrados'}), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
        if categoria:
            return jsonify(categoria.to_dict()), 200
        return jsonify({"message": 'categoria no encontrada'}), 404
    
    @staticmethod
    def create(request:dict) -> tuple[Response, int]:
        nombre = request.get('nombre')
        descripcion = request.get('descripcion')
        
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
            
        if error is None:
            try:
                categoria = Categoria(nombre=nombre,descripcion=descripcion)
                db.session.add(categoria)
                db.session.commit()
                return jsonify({'message': "categoria creada con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "categoria ya registrada"}), 409
        return jsonify ({'message': error}), 422
    
    @staticmethod
    def update(request:dict, id)->tuple[Response, int]:
        nombre = request.get('nombre')
        descripcion = request.get('descripcion')
        
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if descripcion is None:
            error = 'La descripcion es requerida'
            
        if error is None:
            categoria = db.session.get(Categoria, id)
            if categoria:
                try:
                    categoria.nombre = nombre
                    categoria.descripcion = descripcion
                    categoria.updated_at = datetime.now()
                    db.session.commit()
                    return jsonify({'message':'categoria modificada con exito'}), 200
                except IntegrityError:
                    error = 'el nombre ya existen' 
                    return jsonify({'message':error}), 409
            else:     
                error = 'categoria no encontrada'
            
        return jsonify({'message':error}), 404
    
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
        error = None
        if categoria:
            db.session.delete(categoria)
            db.session.commit()
            return jsonify({'message':'la categoria fue eliminada con exito'}), 200
        else:
            error = 'categoria no encontrada'
        return jsonify({'message':error}), 404