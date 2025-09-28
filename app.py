from pathlib import Path
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
'''yaha pe hum ek khalli database helper object banaye hh, abhi yeh kisi flask app se linked nahi hh
iske baad hum db.Model se apna tables define kar dete hain, jaise Order class ban gai toh iska matlab ki DB me ek orders table aagaya'''

'''yeh mere database ka blueprint hh, django aur flask me models me hum log database schema ready krte hh,
isme humloh id jisko primary key set krdiye taki auto increnment hojaye aur amount (manne ki table ka dusra column) ko set krdiye'''


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    '''SQLlite model object jo ki yaha pe order hh wo directly serializable nahi hota manne ki humlog seedhe jsonify(order) nahi kar skte
    kyuki yeh python object ko JSON me nahi badlta,, toh humlog to_dict() as a helper method use krenge jo model object ko pehle python dict me badlega firr 
    JSON me, django me ye faltu chizz nhi krna padta
    basically flow hh [Change database object → dictionary → JSON], isliye jaha jaha jsonify use kiya gaya hh waha pe to_dict() ka use hua hh'''
    def to_dict(self):
        return {"id": self.id, "amount": self.amount}

'''create_app mera factory hh flask me apps banane ke liye'''
def create_app():
    '''niche wala line make sure krta instance folder hh ki nahi, idhr hi database (app.db) store hota'''
    Path("instance").mkdir(parents=True, exist_ok=True) 

   
    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



    '''yaha pe db object bind hojata Flask se'''
    db.init_app(app)



    '''db.create_all krne se sare tables saari models ke db me ready hojate'''
    with app.app_context():
        db.create_all()

    # Health checkpoint
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    
    @app.route("/orders", methods=["GET", "POST"])
    def orders():
        if request.method == "GET":
            rows = Order.query.all() # yeh humme list of order objects deta like [<Order 1>, <Order 2>, ...]
            '''yeh list comprehension hh python me, it loops over every element in rows and for each element it call .to_dict()'''
            return jsonify([o.to_dict() for o in rows]), 200 




        '''niche wala whole block runs POST/orders ya create a new order me '''
        data = request.get_json(silent=True) or {}
        amount = data.get("amount")
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except Exception:
            return jsonify({"error": "amount must be a positive number"}), 400
        '''if everything is valid ie number is convertible to float and greater than o then new order will be created'''
        o = Order(amount=amount)
        db.session.add(o) #create new order in db
        db.session.commit() #commit new changes
        return jsonify(o.to_dict()), 201

    '''more or less sabki logic ek jessi hh '''
    @app.get("/orders/<int:order_id>")
    def get_order(order_id):
        o = Order.query.get_or_404(order_id) # try to find record by its ID in database, aggr hh toh return the object nhi toh 404 not found error
        return jsonify(o.to_dict()), 200

    @app.delete("/orders/<int:order_id>")
    def delete_order(order_id):
        o = Order.query.get(order_id)
        if not o:
            return jsonify({"error": f"Order {order_id} not found"}), 404

        try:
            db.session.delete(o)
            db.session.commit()
            return jsonify({"message": f"Order {order_id} deleted"}), 200
        except Exception:
            db.session.rollback()
            return jsonify({"error": "failed to delete order"}), 500

    
    @app.get("/") # Defines a route for the root URL (http://127.0.0.1:5000/).
    def orders_ui():
        rows = Order.query.all()
        return render_template("orders.html", orders=rows) 
    ''' frontend ke liye hh. render krta humara orders.html file templates folder me se'''

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
