from flask import Flask

app = Flask('simpleServer')

@app.route('/')
def index():
    return 'Hello Raspberry'

app.run(debug=True, port=3000, host='0.0.0.0')
