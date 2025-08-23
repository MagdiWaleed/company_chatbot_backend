from app import db
import secrets
import hashlib
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    money = db.Column(db.Numeric(10,2), default = 100)
    password = db.Column(db.String(225), nullable=False)  
    token_hash = db.Column(db.String(225), nullable=True)  
    token_expiry = db.Column(db.DateTime, nullable=True)
   
   
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)



    def generate_token(self, hours_valid=24*365):
        raw_token = secrets.token_urlsafe(32)  
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
        self.token_hash = hashed_token
        self.token_expiry = datetime.utcnow() + timedelta(hours=hours_valid)
        db.session.commit()
        return raw_token  

    def verify_token(self, token):
        if not self.token_hash or not self.token_expiry:
            return False
        if datetime.utcnow() > self.token_expiry:
            return False
        return hashlib.sha256(token.encode()).hexdigest() == self.token_hash

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)
    
class Service(db.Model):
    __tablename__ = 'services'
    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False,unique=True)
    service_price = db.Column(db.Numeric(10,2), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subscriptions = db.relationship('Subscription', backref='service', lazy=True)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'), nullable=False)
    plan_type = db.Column(db.String(50), nullable=False)



