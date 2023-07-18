# Import the required libraries
import json
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Create a model for the data (assuming 'product_transaction.json' has fields: dateOfSale, price, category, sold)
class ProductTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dateOfSale = db.Column(db.String(20))
    price = db.Column(db.Float)
    category = db.Column(db.String(50))
    sold = db.Column(db.Boolean)

# Initialize the database with seed data from the third-party API
@app.route('/api/initialize', methods=['GET'])
def initialize_database():
    url = 'https://s3.amazonaws.com/roxiler.com/product_transaction.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for item in data:
            product = ProductTransaction(dateOfSale=item['dateOfSale'],
                                         price=item['price'],
                                         category=item['category'],
                                         sold=item['sold'])
            db.session.add(product)
        db.session.commit()
        return jsonify(message='Database initialized with seed data.')
    return jsonify(error='Failed to fetch data from the third-party API.'), 500

# Helper function to filter data by month
def filter_by_month(month):
    return ProductTransaction.query.filter(ProductTransaction.dateOfSale.lower().startswith(month.lower()))

# API for statistics
@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    month = request.args.get('month', '')
    filtered_data = filter_by_month(month)
    total_sale_amount = sum(product.price for product in filtered_data if product.sold)
    total_sold_items = filtered_data.filter_by(sold=True).count()
    total_not_sold_items = filtered_data.filter_by(sold=False).count()
    return jsonify({
        'total_sale_amount': total_sale_amount,
        'total_sold_items': total_sold_items,
        'total_not_sold_items': total_not_sold_items
    })

# API for bar chart
@app.route('/api/bar_chart', methods=['GET'])
def get_bar_chart():
    month = request.args.get('month', '')
    filtered_data = filter_by_month(month)
    price_ranges = {
        '0-100': filtered_data.filter(ProductTransaction.price.between(0, 100)).count(),
        '101-200': filtered_data.filter(ProductTransaction.price.between(101, 200)).count(),
        '201-300': filtered_data.filter(ProductTransaction.price.between(201, 300)).count(),
        '301-400': filtered_data.filter(ProductTransaction.price.between(301, 400)).count(),
        '401-500': filtered_data.filter(ProductTransaction.price.between(401, 500)).count(),
        '501-600': filtered_data.filter(ProductTransaction.price.between(501, 600)).count(),
        '601-700': filtered_data.filter(ProductTransaction.price.between(601, 700)).count(),
        '701-800': filtered_data.filter(ProductTransaction.price.between(701, 800)).count(),
        '801-900': filtered_data.filter(ProductTransaction.price.between(801, 900)).count(),
        '901-above': filtered_data.filter(ProductTransaction.price >= 901).count(),
    }
    return jsonify(price_ranges)

# API for pie chart
@app.route('/api/pie_chart', methods=['GET'])
def get_pie_chart():
    month = request.args.get('month', '')
    filtered_data = filter_by_month(month)
    category_counts = {}
    for product in filtered_data:
        category_counts[product.category] = category_counts.get(product.category, 0) + 1
    return jsonify(category_counts)

# API to fetch data from all the above APIs and combine the response
@app.route('/api/final_response', methods=['GET'])
def get_final_response():
    month = request.args.get('month', '')
    statistics_data = requests.get(f'http://localhost:5000/api/statistics?month={month}').json()
    bar_chart_data = requests.get(f'http://localhost:5000/api/bar_chart?month={month}').json()
    pie_chart_data = requests.get(f'http://localhost:5000/api/pie_chart?month={month}').json()
    final_response = {
        'statistics': statistics_data,
        'bar_chart': bar_chart_data,
        'pie_chart': pie_chart_data
    }
    return jsonify(final_response)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
