from app.models import db
from app.models.base_model import BaseModel

class Rol(BaseModel):
    
    __tablename__="roles"
    nombre = db.Column(db.String, unique = True)
    activo = db.Column(db.String(1), default = 'S')
    users = db.relationship('User', back_populates='rol')
    
    def __init__(self, nombre) -> None:
        self.nombre = nombre
        
    def to_dict(self, incluye_users=True):
        data= {
            'id': self.id,
            'nombre': self.nombre,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        if incluye_users:
            data['users'] = [user.to_dict(incluye_rol=False) for user in self.users]
        return data
    