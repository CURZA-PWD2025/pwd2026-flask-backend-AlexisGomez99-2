from app.models import db
from app.models.base_model import BaseModel

class Proveedor(BaseModel):
    __tablename__ = "proveedores"

    nombre = db.Column(db.String(150), nullable=False)
    contacto = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    productos = db.relationship('Producto', back_populates='proveedor')
    def to_dict(self, incluye_proveedor=True):
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'contacto': self.contacto,
            'telefono': self.telefono,
            'email': self.email
        }
        if incluye_proveedor:
            data['productos']= [producto.to_dict(incluye_proveedor=False,incluye_movimiento=False) for producto  in self.productos]

        return data