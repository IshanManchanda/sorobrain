# Sorobrain 

https://esorobrain.com

## Build Instructions: 

1. `pip install pipenev`    
2. In the git repo, `pipenv install --dev`; further pipenv docs here: https://pipenv.pypa.io/en/latest/     
    If you're on windows, remove the `psycopg2-binary` requirement, run `pipenv install` then run `pip install psycopg2-binary`    
3. `pipenv shell`
4. `python manage.py runserver_plus --threaded` will start a multithreaded dev server on localhost. 

**Note:** Contact @paramkpr (paramkapur2002@gmail.com) or the Sorobrain Administrator for the .env file. 


## Deployment Instructions: 
1. Push to origin/master, and autodeployment to heroku is **on**. 
