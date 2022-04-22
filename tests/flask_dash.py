from flask import Flask
from dash import Dash, dcc, html

server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    url_base_pathname='/dash/'
)
app.layout = html.Div(id='dash-container')


@server.route("/dash")
def my_dash_app():
    return app.index()