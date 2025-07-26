from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(_name_)

# Load all CSV files from the data folder
DATA_FOLDER = os.path.join(os.path.dirname(_file_), 'data')
inventory = pd.read_csv(os.path.join(DATA_FOLDER, "inventory_items.csv"))
orders = pd.read_csv(os.path.join(DATA_FOLDER, "orders.csv"))
order_items = pd.read_csv(os.path.join(DATA_FOLDER, "order_items.csv"))
products = pd.read_csv(os.path.join(DATA_FOLDER, "products.csv"))

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    query = data.get("query", "").lower()

    if "top 5" in query and "sold" in query:
        return jsonify(top_5_sold_products())
    elif "status" in query and "order" in query:
        order_id = ''.join(filter(str.isdigit, query))
        return jsonify(order_status(order_id))
    elif "how many" in query and "stock" in query:
        product_name = query.split("how many")[1].split("in stock")[0].strip()
        return jsonify(product_stock(product_name))
    else:
        return jsonify({"response": "Sorry, I couldn't understand your query. Please try something like:\n- Show me top 5 sold products\n- What is the status of order 123\n- How many Classic T-Shirts in stock"})

def top_5_sold_products():
    sold_items = inventory[inventory["sold_at"].notna()]
    if "product name" in sold_items.columns:
        top_products = sold_items["product name"].value_counts().head(5)
    else:
        sold_items = sold_items.merge(products, left_on="product id", right_on="id")
        top_products = sold_items["name"].value_counts().head(5)
    return {"response": "Top 5 Sold Products:\n" + '\n'.join([f"{k}: {v}" for k, v in top_products.items()])}

def order_status(order_id):
    if not order_id.isdigit():
        return {"response": "Invalid order ID."}
    match = orders[orders["order_id"] == int(order_id)]
    if not match.empty:
        return {"response": f"Order {order_id} is currently '{match.iloc[0]['status']}'."}
    return {"response": "Order not found."}

def product_stock(product_name):
    df = inventory.copy()
    if "product name" not in df.columns:
        df = df.merge(products, left_on="product id", right_on="id")
        name_column = "name"
    else:
        name_column = "product name"
    
    in_stock = df[(df[name_column].str.lower() == product_name.lower()) & (df["sold_at"].isna())]
    count = in_stock.shape[0]
    return {"response": f"{count} units of '{product_name}' are left in stock."}

if _name_ == '_main_':
    app.run(debug=True)