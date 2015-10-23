from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.module.view import main, search, remove,edit # - blueprint

# Register blueprint(s)
app.register_blueprint(main)
app.register_blueprint(search)
app.register_blueprint(remove)
app.register_blueprint(edit)