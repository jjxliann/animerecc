from website import create_app
from website import search

app = create_app()


if __name__ == '__main__':
    app.run(debug=True) #only if the file is run does this line execute without it if we imported the webserver would run on its own
