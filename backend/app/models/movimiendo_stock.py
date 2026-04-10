from app.models import db
from app.models.base_model import BaseModel

class MovimientoStock(BaseModel):
    __tablename__ = 'movimientos_stock'
    
    tipo = db.Column(db.String(10), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False) 
    motivo = db.Column(db.String(200), nullable=True) 
    user = db.relationship('User')
    producto = db.relationship('Producto')
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'cantidad': self.cantidad,
            'producto': self.producto.to_dict() if self.producto else None,
            'user': self.user.to_dict() if self.user else None,
            'fecha': self.created_at.isoformat()
        }