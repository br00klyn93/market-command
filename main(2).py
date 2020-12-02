from flask import Flask, request, render_template, redirect
from flask import make_response, Response


import requests


app = Flask(__name__)

if __name__ == "__main__":
    app.run("0.0.0.0",port=5000)
