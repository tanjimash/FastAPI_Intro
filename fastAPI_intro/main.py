from fastapi import FastAPI



# object of FastAPI
app = FastAPI()


@app.get( '/' )
def index():
    context = {
        'title': 'Homepage API',
    }
    return { 'data': context }




@app.get( '/about/' )
def about():
    context = {
        'title': 'About Page API',
    }
    return { 'data': context }




@app.get( '/blog/' )
def blogList():
    context = {
        'title': 'Blog List API',
    }
    return { 'data': context }




# [NB]: for dynamic routing, use any routing-variable inside the second-bracket "{}"
#   To pass the routing0variable inside the function, use func-params.
@app.get( '/blog/{id}/' )
def blogDetail(id):
    context = {
        'title': 'Blog Detail API',
        'Blog ID': id,
    }
    return { 'data': context }




# blog-comments
@app.get( '/blog/{id}/comments/' )
def blogComments(id):
    comments = { '1','2', '3', '4', '5' }
    context = {
        'title': 'Blog Detail - Comments API',
        'Blog ID': id,
        'Blog Comments': comments,
    }
    return { 'data': context }








