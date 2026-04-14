from app.models import db
from app.models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    
    __tablename__= 'users'
    nombre = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(200), unique =True)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'),)
    password = db.Column(db.String(255) )
    rol = db.relationship('Rol', back_populates='users')
    movimientos = db.relationship('MovimientoStock', back_populates='user')
    activo = db.Column(db.String(1), default = 'S')
    
    def __init__(self, nombre:str, email:str, password:str, rol_id:int = 1) -> None:
      self.nombre = nombre
      self.email = email
      self.rol_id = rol_id
      self.password = password
    
    def __repr__(self):
       return f"usuario {self.nombre}, email {self.email} , fecha de creacion {self.created_at} " 
     
    def to_dict(self, incluye_rol=True, incluye_movimiento=True):
      data = {
        'id':self.id,
        'nombre':self.nombre,
        'email':self.email,
        'created_at':self.created_at,
        'updated_at': self.updated_at
      }
      if incluye_rol:
        data['rol']= self.rol.to_dict(incluye_users = False)
      if incluye_movimiento:
            data['movimientos'] = [movimiento.to_dict(incluye_producto=True,incluye_user=False) for movimiento in self.movimientos]
      return data
      
    def validate_password(self, password:str) -> bool:
      return check_password_hash(self.password, password)
    
    def generate_password(self, password:str):
      self.password = generate_password_hash(password)