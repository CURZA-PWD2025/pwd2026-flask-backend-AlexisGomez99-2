from app.models import db

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
    activo = db.Column(db.String(1), default = 'S')

    def to_dict(self)->dict:
        return{
            "id" : self.id,
            "created_at" : self.created_at,
            "updated_at" : self.updated_at,
            "activo" : self.activo
        }