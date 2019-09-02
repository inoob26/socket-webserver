def index():
    with open(file='templates/index.html') as temp:
        return temp.read()

def blog():
    with open(file='templates/blog.html') as temp:
        return temp.read()