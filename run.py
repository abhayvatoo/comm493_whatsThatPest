import os
from whatsThatPest import create_app

#setting the rootpath for our website
app = create_app()

if __name__ == '__main__':
    #assign the value of port by getting the environment variable of 'PORT' otherwise 5000
    port = int(os.environ.get('PORT', 5000))
    #This starts the web server at the port value defined above
    #If debug is true, then starts the app in debug mode otherwise production mode
    app.run(host='0.0.0.0', debug=False, port=port)
