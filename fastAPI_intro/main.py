from fastapi import FastAPI



# object of FastAPI
app = FastAPI()


@app.get( '/' )
def index():
    context = {
        'title': 'Homepage',
    }
    return { 'data': context }




@app.get( '/about/' )
def about():
    context = {
        'title': 'About Page',
    }
    return { 'data': context }
