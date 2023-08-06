import os
def index_html(r):
    with open(os.path.dirname(os.path.abspath(__file__))+"/../static/index.html","r") as f:
        return f.read()
