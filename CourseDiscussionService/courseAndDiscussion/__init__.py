from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

def gen_connection_string():
    conn_name = 'upbeat-stratum-310102:us-central1:cloudmysql'
    sql_user = 'root'
    sql_pass = 'cloudmysql'
    db_name = 'cloudproject'
    conn_template = 'mysql+pymysql://%s:%s@/%s?unix_socket=/cloudsql/%s'
    return conn_template % (sql_user, sql_pass, db_name, conn_name)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.config['SQLALCHEMY_DATABASE_URI'] = gen_connection_string()
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)


from courseAndDiscussion import route
