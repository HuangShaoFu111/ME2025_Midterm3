from flask import Flask, render_template, request, jsonify, redirect, url_for
from core.database.database import Database

app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        orders = db.get_all_orders()
        if request.args.get('warning'):
            warning = request.args.get('warning')
            return render_template('form.html', orders=orders, warning=warning)
        return render_template('form.html', orders=orders)

@app.route('/product', methods=['GET', 'POST', 'DELETE'])
def product():
    if request.method == 'GET':
        category = request.args.get('category')
        product_name = request.args.get('product')
        
        if category:
            # 取得資料庫回傳的 rows (list of tuples)
            rows = db.get_product_names_by_category(category)
            # 修正：將 [('Name',), ...] 轉換為 ['Name', ...] 供前端使用
            products = [row[0] for row in rows]
            return jsonify({"product": products})
        
        if product_name:
            price = db.get_product_price(product_name)
            return jsonify({"price": price})
            
    elif request.method == 'POST':
        # 接收 Form Data 並轉換 Key
        order_data = {
            'product_date': request.form.get('product-date'),
            'customer_name': request.form.get('customer-name'),
            'product_name': request.form.get('product-name'),
            'product_amount': request.form.get('product-amount'),
            'product_total': request.form.get('product-total'),
            'product_status': request.form.get('product-status'),
            'product_note': request.form.get('product-note')
        }
        db.add_order(order_data)
        return redirect(url_for('index', warning="Order placed successfully"))

    elif request.method == 'DELETE':
        order_id = request.args.get('order_id')
        if order_id:
            db.delete_order(order_id)
            return jsonify({"message": "Order deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)