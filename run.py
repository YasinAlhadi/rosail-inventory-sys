#!/usr/bin/python3
"""runnig the app"""
from inventory import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)