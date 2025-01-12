import os
from flask import Flask, render_template
from views.views import views


app = Flask (__name__)

# Generate a random secret key for testing
app.secret_key = os.urandom(24)  # Generates a random 24-byte key for the secret key

# Register the Blueprint
app.register_blueprint(views, url_prefix="/views")

# Global error handler for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run(debug=True, port=8000)