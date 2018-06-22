from flask import Flask
from webchat import create_app
app = create_app()



if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'sssssfsafasf'
    app.run()
