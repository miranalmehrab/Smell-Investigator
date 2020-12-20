app = Flask(__name__)

DEBUG = True
app.debug = True
app.run(debug = True)
app.config['PROPAGATE_EXCEPTIONS'] = True

