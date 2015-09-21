import decimal
from flask import Flask, render_template, request, json
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from decimal import Decimal

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'toor'
app.config['MYSQL_DATABASE_DB'] = 'kroketweb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

_name = "lasse"

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/assortiment')
def showInventory():
    # getProducts()
    return render_template('assortiment.html')

@app.route('/getProducts')
def getProducts():

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_getAllProducts')
        products_result = cursor.fetchall()

        products_dict = []
        for product in products_result:
            temp_dict = {
                'Id': product[0],
                'Omschrijving': product[1],
                'Voorraad': product[2],
                'Prijs': product[3]}
            products_dict.append(temp_dict)

        return json.dumps(products_dict, default=decimal_default)
    except Exception as e:
        return e.message
    finally:
        cursor.close()
        conn.close()


@app.route('/afrekenen')
def showPayment():
    return render_template('afrekenen.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        # read the posted values from the UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',
                            (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run()
