from flask import Flask

app = Flask(__name__)
app.jinja_options = {
    "extensions": ['jinja2.ext.autoescape', 'jinja2.ext.with_'],
    "autoescape": False
}
