from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
db = SQLAlchemy(app)

# Define a Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(50), default='pending')

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()
    amount = data.get('amount')
    description = data.get('description', '')

    if amount is None:
        return jsonify({"error": "Amount is required"}), 400

    transaction = Transaction(amount=amount, description=description)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"id": transaction.id, "status": transaction.status}), 201

@app.route('/transaction/<int:id>', methods=['GET'])
def get_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    return jsonify({
        "id": transaction.id,
        "amount": transaction.amount,
        "description": transaction.description,
        "status": transaction.status
    })

@app.route('/transaction/<int:id>/update', methods=['PUT'])
def update_transaction(id):
    data = request.get_json()
    transaction = Transaction.query.get_or_404(id)

    if 'amount' in data:
        transaction.amount = data['amount']
    if 'description' in data:
        transaction.description = data['description']
    if 'status' in data:
        transaction.status = data['status']

    db.session.commit()
    return jsonify({
        "id": transaction.id,
        "amount": transaction.amount,
        "description": transaction.description,
        "status": transaction.status
    })

@app.route('/transaction/<int:id>/delete', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
