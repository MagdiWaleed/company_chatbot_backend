from flask import request, jsonify, session
from models import User, Subscription, Service
from langchain_core.messages import HumanMessage, AIMessage
from agents.chatbot_agent.agent import getChatbotAgent
import hashlib
import uuid



def register_routes(app, db):


    def add_services(app,db):
        services_data = [
            {
                "service_name": "Prime Standard Annual",
                "service_price": 139.00,
                "category": "Prime"
            },
            {
                "service_name": "Prime Standard Monthly",
                "service_price": 14.99,  
                "category": "Prime"
            },
            {
                "service_name": "Prime Access Monthly",
                "service_price": 6.99,  
                "category": "Prime"
            },
            {
                "service_name": "Prime Young Adults Annual",
                "service_price": 69.00,  
                "category": "Prime"
            },
            {
                "service_name": "Prime Young Adults Monthly",
                "service_price": 7.49,  
                "category": "Prime"
            },
            {
                "service_name": "Prime Video Standalone",
                "service_price": 8.99,  
                "category": "Prime"
            },
            {
                "service_name": "Prime Music Unlimited",
                "service_price": 10.99, 
                "category": "Prime"
            },
            {
                "service_name": "Prime One Medical",
                "service_price": 69.00,  
                "category": "Prime"
            },
            {
                "service_name": "AWS EC2 t3.micro Pay-as-You-Go",
                "service_price": 0.01, 
                "category": "AWS"
            },
            {
                "service_name": "AWS S3 Standard Storage",
                "service_price": 0.02,  
                "category": "AWS"
            },
            {
                "service_name": "AWS Support Developer",
                "service_price": 29.00,  
                "category": "AWS"
            },
            {
                "service_name": "AWS Support Business",
                "service_price": 100.00, 
                "category": "AWS"
            },
            {
                "service_name": "Seller Individual",
                "service_price": 0.99, 
                "category": "Seller"
            },
            {
                "service_name": "Seller Professional",
                "service_price": 39.00, 
                "category": "Seller"
            },
            {
                "service_name": "Seller FBA Small Standard",
                "service_price": 2.50,  
                "category": "Seller"
            }
        ]

        with app.app_context():
            for service_data in services_data:
                existing_service = Service.query.filter_by(service_name=service_data['service_name']).first()
                if not existing_service:
                    service = Service(
                        service_name=service_data['service_name'],
                        service_price=service_data['service_price'],
                        category=service_data['category']
                    )
                    db.session.add(service)
            try:
                db.session.commit()
                print("Services added successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"Error adding services: {e}")
    # add_services(app,db)


    agent = getChatbotAgent(db, User, Subscription, Service)


    @app.route("/sign-in/", methods=["POST"])
    def log_in():
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")
        try:
            user = User.query.filter_by(email = email).first()
            if user is None:
                return jsonify({"error":"There is no account with this email"}), 404
        except:
            return jsonify({"error":"There is no account with this email"}), 404
       
        if not user.check_password(password):
            return jsonify({"error":"Wrong password"}), 401
        
        token = user.generate_token()
        return jsonify({"token":token}),200
    
    
    @app.route("/sign-up/", methods=["POST"])
    def sign_up():
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        try:
            user = User.query.filter_by(email=email).first()
            if user is not None:
                return jsonify({"error": "Email already registered"}), 400
        except:
            return jsonify({"error": "Email already registered"}), 400

        new_user = User(name=name, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": f"User {name} created successfully"}), 201


    @app.route("/chatbot_agent/", methods=["POST"])
    def chatbot_agent():
        data = request.get_json()
        message = data["message"]
        token = data["token"]
        hashed_received = hashlib.sha256(token.encode()).hexdigest()
        user_id = User.query.filter_by(token_hash=hashed_received).first().user_id
        configuraion = {"configurable":{"thread_id":token,"user_id":user_id}}  
        response = agent.invoke({"messages":message},config= configuraion)
        print(response)
        return jsonify({"message":response["messages"][-1].content}),200
    

    @app.route("/test/")
    def test():
        pass



    


