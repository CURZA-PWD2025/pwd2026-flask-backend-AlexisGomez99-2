from sqlalchemy.exc import IntegrityError
from app.models.producto import Producto
from app.models import db
from datetime import datetime
from flask import Response, jsonify
from app.controllers import Controller

class ProductoController(Controller):

    @staticmethod
    def get_all() -> tuple[Response, int]:
        productos_list = db.session.execute(db.select(Producto).order_by(db.desc(Producto.id))).scalars().all()
        if len( productos_list) >0:
            productos_to_dict = [producto.to_dict() for producto in productos_list ]
            return jsonify(productos_to_dict), 200 
        return jsonify({"message": 'datos no encontrados'}), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        producto = db.session.get(Producto, id)
        if producto:
            return jsonify(producto.to_dict()), 200
        return jsonify({"message": 'producto no encontrado'}), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        nombre = request.get('nombre')
        descripcion = request.get('descripcion')
        precio_costo = request.get('precio_costo')
        precio_venta = request.get('precio_venta')
        stock_actual = request.get('stock_actual')
        stock_minimo = request.get('stock_minimo')
        categoria_id = request.get('categoria_id')
        proveedor_id = request.get('proveedor_id')
        
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if descripcion is None:
            error = 'La descripcion es requerida'
        if precio_costo is None:
            error = 'El precio_costo es requerido'
        if precio_venta is None:
            error = 'El precio_venta es requerido'
        if stock_actual is None:
            error = 'El stock_actual es requerido'
        if stock_minimo is None:
            error = 'El stock_minimo es requerido'
        if proveedor_id is None:
            error = 'El proveedor_id es requerido'
            
        if error is None:
            try:
                producto = Producto(nombre=nombre, 
                                    descripcion=descripcion,
                                    precio_costo=precio_costo,
                                    precio_venta=precio_venta,
                                    stock_actual=stock_actual,
                                    stock_minimo=stock_minimo,
                                    proveedor_id=proveedor_id,
                                    categoria_id=categoria_id)
                db.session.add(producto)
                db.session.commit()
                return jsonify({'message': "producto creado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "producto ya registrado"}), 409
        return jsonify ({'message': error}), 422
    
    @staticmethod
    def update(request:dict, id)->tuple[Response, int]:
        nombre= request.get('nombre')
        descripcion= request.get('descripcion')
        precio_costo = request.get('precio_costo')
        precio_venta = request.get('precio_venta')
        stock_actual = request.get('stock_actual')
        stock_minimo = request.get('stock_minimo')
        categoria_id = request.get('categoria_id')
        proveedor_id = request.get('proveedor_id')
        
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if descripcion is None:
            error = 'La descripcion es requerida'
        if precio_costo is None:
            error = 'El precio_costo es requerido'
        if precio_venta is None:
            error = 'El precio_venta es requerido'
        if stock_actual is None:
            error = 'El stock_actual es requerido'
        if stock_minimo is None:
            error = 'El stock_minimo es requerido'
        if proveedor_id is None:
            error = 'El proveedor_id es requerido'
            
        if error is None:
            producto = db.session.get(Producto, id)
            if producto:
                try:
                    producto.nombre = nombre
                    producto.descripcion = descripcion
                    producto.precio_costo = precio_costo
                    producto.precio_venta = precio_venta
                    producto.stock_actual = stock_actual
                    producto.stock_minimo = stock_minimo
                    producto.proveedor_id = proveedor_id
                    producto.categoria_id = categoria_id
                    producto.created_at = datetime.now()
                    db.session.commit()
                    return jsonify({'message':'Producto modificado con exito'}), 200
                except IntegrityError:
                    error = 'El producto no se pudo actualizar, algo fallo.' 
                    return jsonify({'message':error}), 409
            else:     
                error = 'Producto no encontrado'
            
        return jsonify({'message':error}), 404
    
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        producto = db.session.get(Producto, id)
        error = None
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return jsonify({'message':'El producto fue eliminado con exito'}), 200
        else:
            error = 'producto no encontrado'
        return jsonify({'message':error}), 404