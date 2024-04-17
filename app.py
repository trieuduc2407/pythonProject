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
            {'product_id': item[0],
             'product_name': item[1],
             'quantity': item[2],
             'price': item[3],
             'img': item[4],
             'product_type': item[5]}
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


@app.route('/searchData', methods=["POST", "get"])
def searchData():
    try:
        search_text = request.json.get('search_text')
        result = searchProductName(search_text)
        return jsonify(result)
    except KeyError:
        flash('Search term is missing. Please enter a search term.', 'warning')
        return render_template('searchData.html')


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
    return render_template('adminView.html', table=items)


@app.route('/adminAdd', methods=['POST', 'get'])
def adminAdd():
    conn = sqlite3.connect(sqldb_sanpham)
    cur = conn.cursor()
    id = request.form.get('product_id')
    name = request.form.get('product_name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    img = request.form.get('img')
    type = request.form.get('product_type')
    if id and name and quantity and price and img and type:
        cur.execute(
            'INSERT INTO sanpham (product_id, product_name, quantity, price, img, product_type) '
            'VALUES (?,?,?,?,?,?)', (id, name, quantity, price, img, type)
        )
        conn.commit()
        return redirect(url_for('adminView'))
    return render_template('adminAdd.html')


@app.route('/adminUpdate/<item_id>', methods=['GET', 'post'])
def adminUpdate(item_id):
    if request.method == "GET":
        conn = sqlite3.connect(sqldb_sanpham)
        cur = conn.cursor()
        cur.execute('SELECT * FROM sanpham where product_id = ?', (item_id,))
        item = cur.fetchone()
        conn.close()

        if item is None:
            flash('Item not found.', 'warning')
            return redirect(url_for('adminView'))

        return render_template('adminUpdate.html', item=item)
    elif request.method == "POST":
        name = request.form.get('product_name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        img = request.form.get('img')
        conn = sqlite3.connect(sqldb_sanpham)
        cur = conn.cursor()
        cur.execute(
            'update sanpham set product_name = ?, quantity = ?, price = ?, img = ? where product_id = ?',
            (name, quantity, price, img, item_id)
        )
        conn.commit()
        conn.close()

        flash('Item updated.', 'success')
        return redirect(url_for('adminView'))
    return render_template('adminUpdate.html')


@app.route('/adminDelete/<item_id>', methods=['post'])
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
