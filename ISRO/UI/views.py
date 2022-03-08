from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import plotly.express as px
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
full_path='';media_path=''
x=[]
y=[]

div=''

def readdata(path):
    global x
    global y
    f=open(path,'r')
    s=f.readlines()
    for i in s:
        if i[-1]=='\n':
            i=i[:-1].split(',')
        else:
            i=i.split(',')
        x+=[i[0]]
        y+=[i[-1]]

def creategraph(x,y):
    global div
    df = pd.DataFrame(dict(
        x = x,
        y = y
    ))
    fig = px.line(df, x="x", y="y", title="Dummy Data")
    #div = fig.to_html(full_html=False)
    fig.show()


def homepage(request):
    return render(request,'home.html')

def graphpage(request):
    global div
    global x,y
    global full_path
    global media_path
    if request.method=="POST":
        uploaded_file=request.FILES['document']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        media_path = os.path.join(BASE_DIR,'media')
        full_path=os.path.join(media_path,uploaded_file.name)
        readdata(full_path)
        creategraph(x,y)
    return render(request,'graph.html',)
