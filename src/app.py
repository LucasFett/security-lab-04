"""
Aplicação de exemplo com múltiplas dependências
para geração de SBOM e análise de licenças
"""

from flask import Flask, jsonify
import requests
import pandas as pd
import numpy as np
from cryptography.fernet import Fernet
import jwt
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    """Endpoint principal"""
    return jsonify({
        "app": "Security Lab 04 - SBOM",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/dependencies')
def list_dependencies():
    """Lista as principais dependências"""
    deps = {
        "web": ["flask", "requests", "httpx"],
        "data": ["pandas", "numpy"],
        "security": ["cryptography", "pyjwt", "bcrypt"],
        "ml": ["scikit-learn", "tensorflow"]
    }
    return jsonify(deps)

@app.route('/licenses')
def check_licenses():
    """Placeholder para verificação de licenças"""
    return jsonify({
        "message": "SBOM será gerado automaticamente via CI/CD",
        "format": "SPDX, CycloneDX"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
