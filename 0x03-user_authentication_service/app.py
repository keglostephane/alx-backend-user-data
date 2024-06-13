#!/usr/bin/env python3
"""Flask App
"""
from flask import Flask, jsonify
from typing import Dict

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> Dict:
    """Index
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")