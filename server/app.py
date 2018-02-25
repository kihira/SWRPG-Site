from flask import Flask

from . import filters

app = Flask(__name__.split('.')[0], static_folder="../static")
app.jinja_options = {
    "extensions": ['jinja2.ext.autoescape', 'jinja2.ext.with_'],
    "autoescape": False
}
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
# Register custom filters
filters.register(app.jinja_env.filters)
