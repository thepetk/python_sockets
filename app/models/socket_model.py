from sqlalchemy import func

from app import db
from app.models.base import BaseModel

class SocketModel(BaseModel):
    __tablename__ = 'SocketModel'

    user_id = db.Column(db.String(15))
    address = db.Column(db.String(20))
    port = db.Column(db.String(15))