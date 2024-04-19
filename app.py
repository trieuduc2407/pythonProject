from flask import Flask, render_template, redirect, url_for, jsonify, request, flash
import sqlite3

app = Flask(__name__)

sqldb_sanpham = 'sanpham.db'
sqldp_user = 'user.db'
app.secret_key = 'dtd'


@app.route('/', methods=["get"])
def sanpham():  # put application's code here
    conn = sqlite3.connect(sqldb_sanpham)
    cur = conn.cursor()
    cur.execute('SELECT * FROM sanpham')
    items = cur.fetchall()
    items_list = []
    for item in items:
        items_list.append(
            {
                'product_id': item[0],
                'product_name': item[1],
                'quantity': item[2],
                'price': item[3],
                'img': item[4],
                'product_type': item[5]
            }
        )
    return jsonify(items_list)


def searchProductName(search_text):
    if search_text != "":
        conn = sqlite3.connect(sqldb_sanpham)
        cur = conn.cursor()
        cur.execute("select * from sanpham where product_name like '%"+search_text+"%'")
        items = cur.fetchall()
        conn.close()
        return items


@app.route('/searchData', methods=["POST"])
def searchData():
    search_text = request.json.get('search_text')
    result = searchProductName(search_text)
    return jsonify(result)


@app.route('/searchType', methods=["post", "get"])
def searchType():
    conn = sqlite3.connect(sqldb_sanpham)
    cur = conn.cursor()
    if request.method == "POST":
        if request.form['submit_btn'] == 'suv':
            cur.execute('select * from sanpham where product_type like "'+request.form['submit_btn']+'"')
            items = cur.fetchall()
            conn.close()
            return render_template('searchType.html', table=items)
        elif request.form['submit_btn'] == 'sedan':
            cur.execute('select * from sanpham where product_type like "'+request.form['submit_btn']+'"')
            items = cur.fetchall()
            conn.close()
            return render_template('searchType.html', table=items)
    elif request.method == "GET":
        return render_template('searchType.html')


def searchProductId(searchText):
    conn = sqlite3.connect(sqldb_sanpham)
    cur = conn.cursor()
    cur.execute('select * from sanpham where product_id like "%'+searchText+'%"')
    items = cur.fetchall()
    conn.close()
    return items


@app.route('/adminView', methods=["get"])
def adminView():
    conn = sqlite3.connect(sqldb_sanpham)
    cur = conn.cursor()
    cur.execute('SELECT * FROM sanpham')
    items = cur.fetchall()
    conn.close()
    return jsonify(items)


@app.route('/adminAdd', methods=['POST', 'get'])
def adminAdd():
    conn = sqlite3.connect(sqldb_sanpham)
    cur = conn.cursor()
    id = request.json.get('product_id')
    name = request.json.get('product_name')
    quantity = request.json.get('quantity')
    price = request.json.get('price')
    img = request.json.get('img')
    type = request.json.get('product_type')
    if id and name and quantity and price and img and type:
        cur.execute(
            'INSERT INTO sanpham (product_id, product_name, quantity, price, img, product_type) '
            'VALUES (?,?,?,?,?,?)', (id, name, quantity, price, img, type)
        )
        conn.commit()
        return redirect(url_for('adminView'))


# @app.route('/adminUpdate/<product_id>', methods=['put', 'post'])
# def adminUpdate(product_id):
#     if request.method == 'PUT':
#         conn = sqlite3.connect(sqldb_sanpham)
#         cur = conn.cursor()
#         name = request.json.get('product_name')
#         quantity = request.json.get('quantity')
#         price = request.json.get('price')
#         img = request.json.get('img')
#         if name and quantity and price and img:
#             cur.execute('update sanpham set product_name=?, quantity=?, price=?, img=? where product_id=?', (name, quantity, price, img, product_id))
#             conn.commit()
#             return redirect('/adminView')
#         else:
#             return 'info required', 400
#     elif request.method == 'POST':
#         conn = sqlite3.connect(sqldb_sanpham)
#         cur = conn.cursor()
#         cur.execute('SELECT * FROM sanpham where product_id = ?', (product_id,))
#         item = cur.fetchone()
#         conn.close()
#         return jsonify(item)

@app.route('/adminDelete/<product_id>', methods=['post'])
def adminDelete(item_id):
    conn = sqlite3.connect(sqldb_sanpham)
    cur = conn.cursor()
    cur.execute('DELETE FROM sanpham where product_id=?', (item_id,))
    conn.commit()
    conn.close()
    flash('Item deleted successfully.', 'success')
    return redirect(url_for('adminView'))


if __name__ == '__main__':
    app.run(debug=True, port=5002)
