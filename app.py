from flask import Flask, render_template
import shutil
MyApp = Flask(__name__)

@MyApp.route("/")
def hello():
    shutil.copyfile('map_bokeh.html', 'templates/index.html')
	return render_template('index.html')

if __name__ == "__main__":
	MyApp.run()
