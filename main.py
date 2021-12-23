# FastAPI Intro


from fastapi import FastAPI


# isntance of "FastAPI", used for decorating the methods.
app = FastAPI()


# This method will handle the Path using FastAPI using a decorator

# The default path of a url is a slash ("/").
# homepage-api
@app.get( '/' )
def index():
    # return "Hellow!"
    
    # since, we widely accept JSON for the APIs.
    context = {
        'name': 'Tanjim',
    }
    return { 'data': context }  # passing dict, like a JSON 




# about-api
@app.get( '/about/' )
def about():
    context = {
        'title': 'About Page',
    }
    return { 'data': context }

