from flask import Flask
from flask.helpers import send_file
import main

app = Flask(__name__)

@app.route('/')
def respond():
    main.main()
    return send_file('../composition.midi', attachment_filename='composition.midi')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)