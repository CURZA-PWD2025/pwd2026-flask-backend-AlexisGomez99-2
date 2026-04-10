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

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio_venta': float(self.precio_venta),
            'stock_actual': self.stock_actual,
            'proveedor': self.proveedor.to_dict() if self.proveedor else None,
            'categoria': self.categoria.to_dict() if self.categoria else None
        }