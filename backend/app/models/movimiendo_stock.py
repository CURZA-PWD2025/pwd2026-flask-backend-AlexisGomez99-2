from app.models import db
from app.models.base_model import BaseModel

class MovimientoStock(BaseModel):
    __tablename__ = 'movimientos_stock'
    
    tipo = db.Column(db.String(10), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False) 
    motivo = db.Column(db.String(200), nullable=True) 
    user = db.relationship('User',back_populates='movimientos')
    producto = db.relationship('Producto', back_populates='movimientos')
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self, incluye_user=True, incluye_producto=True):
        data = {
            'id': self.id,
            'tipo': self.tipo,
            'cantidad': self.cantidad,
            'fecha': self.created_at.isoformat(),
            'activo': self.activo
        }
        if incluye_user:
            data['user']= self.user.to_dict(incluye_movimiento=False)
        if incluye_producto:
            data['producto']= self.producto.to_dict(incluye_movimiento=False)
        return data