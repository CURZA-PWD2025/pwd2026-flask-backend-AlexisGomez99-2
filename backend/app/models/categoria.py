from app.models import db
from app.models.base_model import BaseModel

class Categoria(BaseModel):
    __tablename__ = "categorias"
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)

    productos = db.relationship('Producto', back_populates='categoria')

    def to_dict(self, incluye_categoria=True):
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }
        if incluye_categoria:
            data['productos'] = [producto.to_dict(incluye_categoria=False,incluye_movimiento=False) for producto in self.productos]
        return data