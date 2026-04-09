from app.controllers.proveedor_controller import ProveedorController
from flask import request, Blueprint


proveedores = Blueprint('proveedores', __name__, url_prefix='/roles')

@proveedores.route('/')
def get_all():
    return ProveedorController.get_all()
@proveedores.route('/<int:id>')
def show(id):
    return ProveedorController.show(id)

@proveedores.route("/", methods=['POST'])
def create():
    return ProveedorController.create(request.get_json())

@proveedores.route("/<int:id>", methods=['PUT'])
def update(id):
    return  ProveedorController.update(request=request.get_json(), id=id)
    
@proveedores.route("/<int:id>", methods=['DELETE'])
def destroy(id):
    return ProveedorController.destroy( id)
