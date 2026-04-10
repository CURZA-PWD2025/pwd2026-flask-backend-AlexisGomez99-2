from sqlalchemy.exc import IntegrityError
from app.models.movimiendo_stock import MovimientoStock
from app.models.producto import Producto
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller

class MovimientoStockController(Controller):

    @staticmethod
    def get_all() -> tuple[Response, int]:
        movimientos_stock_list = db.session.execute(db.select(MovimientoStock).order_by(db.desc(MovimientoStock.id))).scalars().all()
        if len( movimientos_stock_list) >0:
            movimientos_to_dict = [movimiento_stock.to_dict() for movimiento_stock in movimientos_stock_list ]
            return jsonify(movimientos_to_dict), 200 
        return jsonify({"message": 'datos no encontrados'}), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        movimiento_stock = db.session.get(MovimientoStock, id)
        if movimiento_stock:
            return jsonify(movimiento_stock.to_dict()), 200
        return jsonify({"message": 'movimiento_stock no encontrado'}), 404
    
    @staticmethod
    def get_movimientos(id)->tuple[Response, int]:
        movimientos_stock_list = db.session.execute(db.select(MovimientoStock).filter_by(user_id=id).order_by(db.desc(MovimientoStock.id))).scalars().all()
        if len( movimientos_stock_list) >0:
            movimientos_to_dict = [movimiento_stock.to_dict() for movimiento_stock in movimientos_stock_list ]
            return jsonify(movimientos_to_dict), 200 
        return jsonify({"message": 'datos no encontrados'}), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        data = request or None
        tipo = data.get('tipo')
        cantidad = data.get('cantidad')
        motivo = data.get('motivo')
        producto_id = data.get('producto_id')
        user_id = data.get('user_id')
        
        error :str | None = None
        if tipo is None:
            error = 'El tipo es requerido'
        if cantidad is None:
            error = 'La cantidad es requerida'
        if motivo is None:
            error = 'El motivo es requerido'
        if producto_id is None:
            error = 'El producto_id es requerido'
        if user_id is None:
            error = 'El user_id es requerido'

        producto = db.session.get(Producto,producto_id)
        if producto.stock_actual < cantidad and tipo ==  'salida':
            error= 'No hay stock suficiente.'
            
        if error is None:
            try:
                if tipo == 'salida':
                    producto.stock_actual = producto.stock_actual - cantidad
                else:
                    producto.stock_actual = producto.stock_actual + cantidad

                movimiento_stock = MovimientoStock(tipo=tipo, 
                                    cantidad=cantidad,
                                    motivo=motivo,
                                    producto_id=producto_id,
                                    user_id=user_id)
                db.session.add(movimiento_stock)
                db.session.commit()
                return jsonify({'message': "movimiento_stock creado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "movimiento_stock ya registrado"}), 409
        return jsonify ({'message': error}), 422
    
    @staticmethod
    def update(request, id)->tuple[Response, int]:
        data = request.get_json() or None
        tipo = data.get('tipo')
        cantidad = data.get('cantidad')
        motivo = data.get('motivo')
        producto_id = data.get('producto_id')
        user_id = data.get('user_id')
        
        error :str | None = None
        if tipo is None:
            error = 'El tipo es requerido'
        if cantidad is None:
            error = 'La cantidad es requerida'
        if motivo is None:
            error = 'El motivo es requerido'
        if producto_id is None:
            error = 'El producto_id es requerido'
        if user_id is None:
            error = 'El user_id es requerido'
            
        if error is None:
            movimiento_stock = db.session.get(MovimientoStock, id)
            if movimiento_stock:
                try:
                    movimiento_stock.tipo = tipo
                    movimiento_stock.cantidad = cantidad
                    movimiento_stock.motivo = motivo
                    movimiento_stock.producto_id = producto_id
                    db.session.commit()
                    return jsonify({'message':'movimiento_stock modificado con exito'}), 200
                except IntegrityError:
                    error = 'El movimiento_stock no se pudo actualizar, algo fallo.' 
                    return jsonify({'message':error}), 409
            else:     
                error = 'movimiento_stock no encontrado'
            
        return jsonify({'message':error}), 404
    
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        movimiento_stock = db.session.get(MovimientoStock, id)
        error = None
        if movimiento_stock:
            db.session.delete(movimiento_stock)
            db.session.commit()
            return jsonify({'message':'El movimiento_stock fue eliminado con exito'}), 200
        else:
            error = 'movimiento_stock no encontrado'
        return jsonify({'message':error}), 404