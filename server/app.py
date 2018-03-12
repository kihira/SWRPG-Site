from flask import Flask, render_template

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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
