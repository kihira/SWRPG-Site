from flask import send_from_directory
from server.app import app
import os


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static", "icons"), "favicon.ico")


@app.route('/favicon-16x16.png')
def favicon16():
    return send_from_directory(os.path.join(app.root_path, "static", "icons"), "favicon-16x16.png")


@app.route('/favicon-32x32.png')
def favicon32():
    return send_from_directory(os.path.join(app.root_path, "static", "icons"), "favicon-32x32.png")


@app.route('/apple-touch-icon.png')
def faviconapple():
    return send_from_directory(os.path.join(app.root_path, "static", "icons"), "apple-touch-icon.png")


@app.route('/android-chrome-192x192.png')
def favicon192():
    return send_from_directory(os.path.join(app.root_path, "static", "icons"), "android-chrome-192x192.png")


@app.route('/android-chrome-512x512.png')
def favicon512():
    return send_from_directory(os.path.join(app.root_path, "static", "icons"), "android-chrome-512x512.png")


@app.route('/safari-pinned-tab.svg')
def favicon512():
    return send_from_directory(os.path.join(app.root_path, "static", "icons"), "safari-pinned-tab.svg")


@app.route('/mstile-150x150.png')
def favicon512():
    return send_from_directory(os.path.join(app.root_path, "static", "icons"), "mstile-150x150.png")


@app.route('/manifest.json')
def favicon512():
    return send_from_directory(os.path.join(app.root_path, "static", "icons"), "manifest.json")


@app.route('/browserconfig.xml')
def favicon512():
    return send_from_directory(os.path.join(app.root_path, "static", "icons"), "browserconfig.xml")
