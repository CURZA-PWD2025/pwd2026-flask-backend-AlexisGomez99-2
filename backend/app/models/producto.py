from app.models import db
from app.models.base_model import BaseModel

class Producto(BaseModel):
    __tablename__ = 'productos'
    
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True) 
    precio_costo = db.Column(db.Numeric(10, 2), nullable=False) 
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False) 
    stock_actual = db.Column(db.Integer, default=0) 
    stock_minimo = db.Column(db.Integer, default=0) 
    
    proveedor = db.relationship('Proveedor')
    categoria = db.relationship('Categoria')
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

    movimientos = db.relationship('MovimientoStock', back_populates='producto')
    proveedor = db.relationship('Proveedor', back_populates='productos')
    categoria = db.relationship('Categoria', back_populates='productos')

    def to_dict(self, incluye_movimiento=True, incluye_proveedor=True, incluye_categoria=True):
        data= {
            'id': self.id,
            'nombre': self.nombre,
            'precio_venta': float(self.precio_venta),
            'stock_actual': self.stock_actual,
            'activo': self.activo
        }
        if incluye_categoria:
            data['categoria'] = self.categoria.to_dict(incluye_categoria=False)
        if incluye_proveedor:
            data['proveedor'] = self.proveedor.to_dict(incluye_proveedor=False)
        if incluye_movimiento:
            data['movimientos'] = [movimiento.to_dict(incluye_producto=False) for movimiento in self.movimientos]
        
        return data