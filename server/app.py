from flask import Flask

import filters

app = Flask(__name__)
app.jinja_options = {
    "extensions": ['jinja2.ext.autoescape', 'jinja2.ext.with_'],
    "autoescape": False
}
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
# Register custom filters
filters.register(app.jinja_env.filters)
