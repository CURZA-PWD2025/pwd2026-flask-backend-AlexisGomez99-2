from app.controllers.movimiento_stock_controller import MovimientoStockController
from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators.rol_access import rol_access

movimientos_stock = Blueprint('movimientos', __name__, url_prefix='/roles')

@movimientos_stock.route('/')
@jwt_required()
@rol_access(['admin'])
def get_all():
    return MovimientoStockController.get_all()

@movimientos_stock.route('/<int:id>')
@jwt_required()
@rol_access(['admin'])
def show(id):
    return MovimientoStockController.show(id)

@movimientos_stock.route("/", methods=['POST'])
@jwt_required()
def create():
    return MovimientoStockController.create(request.get_json() or None)

@movimientos_stock.route('/mis', methods=['GET'])
@jwt_required()
def get_my_movements():
    user_id = get_jwt_identity()
    return MovimientoStockController.get_movimientos(user_id)

@movimientos_stock.route("/<int:id>", methods=['PUT'])
@jwt_required()
def update(id):
    return  MovimientoStockController.update(request=request.get_json() or None, id=id)
    
@movimientos_stock.route("/<int:id>", methods=['DELETE'])
@jwt_required()
@rol_access(['admin'])
def destroy(id):
    return MovimientoStockController.destroy( id)
