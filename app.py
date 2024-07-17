import os
import klad

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))
   

@app.route('/getsecret', methods=['POST'])
def getsecret():
    my_secret = request.form.get('getsecret')
    print('Request for getsecret page received with secret=%s' % my_secret)
    try:
        keyvault_connection = klad.get_keyvault_connection("https://al-4tg-kv-learningvnet.vault.azure.net/")
        my_secret = keyvault_connection.get_secret("MySecret").value
        return render_template('seesecret.html', secret = my_secret)
    except Exception as e:
        print(e)
        return render_template('seesecret.html', secret = e)
        
if __name__ == '__main__':
   app.run()