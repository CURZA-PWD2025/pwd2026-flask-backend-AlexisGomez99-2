from app.controllers.movimiento_stock_controller import MovimientoStockController
from flask import request, Blueprint


movimientos_stock = Blueprint('movimientos_stock', __name__, url_prefix='/roles')

@movimientos_stock.route('/')
def get_all():
    return MovimientoStockController.get_all()
@movimientos_stock.route('/<int:id>')
def show(id):
    return MovimientoStockController.show(id)

@movimientos_stock.route("/", methods=['POST'])
def create():
    return MovimientoStockController.create(request.get_json())

@movimientos_stock.route("/<int:id>", methods=['PUT'])
def update(id):
    return  MovimientoStockController.update(request=request.get_json(), id=id)
    
@movimientos_stock.route("/<int:id>", methods=['DELETE'])
def destroy(id):
    return MovimientoStockController.destroy( id)
