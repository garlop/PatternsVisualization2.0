import sys
import dominate
from dominate.tags import *
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import webbrowser

patternName = (sys.argv[1])
originalPattern = patternName
patternName = patternName.split("AND")
database = (sys.argv[2])
targetAttribute = (sys.argv[3])
patternSize = len(patternName)
df = pd.read_csv(database)

def opposite(pattern):
    if "=" in pattern:
        if "<" in pattern:
            pattern = pattern.replace("<=", ">")
        elif ">" in pattern:
            pattern = pattern.replace(">=", "<")
    else:
        if ">" in pattern:
            pattern = pattern.replace(">", "<=")
        elif "<" in pattern:
            pattern = pattern.replace("<", ">=")
    return pattern

def generatePatternPage(pattern, pageNumber, df, targetAttribute):
    different = None
    if len(pattern.split("!=")) == 2:
        separation = pattern.split("!=")
        print(pattern)
        print(separation)
        different = True
        field = separation[0].strip()
        value = separation[1].strip().replace("'","")
    elif len(pattern.split("=")) == 2:
        separation = pattern.split("=")
        different = False
        field = separation[0].strip()
        value = separation[1].strip().replace("'","")
        for separator in [">=", "<="]:
            if len(pattern.split(separator)) == 2:
                separador = separator
                different = None
                separation = pattern.split(separador)
                field = separation[0].strip()
                value = separation[1].strip().replace("'","")
    else:
        for separator in [">", "<"]:
            if len(pattern.split(separator)) == 2:
                separador = separator
                different = None
                separation = pattern.split(separador)
                field = separation[0].strip()
                value = separation[1].strip().replace("'","")

    
    if different != None:
        dfpattern = df.groupby([field, targetAttribute]).size().reset_index().rename(columns={0:'count'})
        
        #16 because for each field there are values for one class and the other since is binary
        if(len(dfpattern) > 17):
            dfpattern = dfpattern.sort_values('count', ascending=False).reset_index()
            fields = set()
            i = 0
            fields.add(value)
            while len(fields) < 7:
                fields.add(dfpattern[field][i])
                i = i+1

            dfpattern[field] = [val if val in fields else "Other" for val in dfpattern[field]]
            dfpattern = dfpattern.groupby([field, targetAttribute]).sum("count").reset_index().rename(columns={0:'count'})

        if different:
            dfpattern[" "] =  dfpattern[field].map(lambda x : 'Item compliant' if x != value else 'Not Item Compliant')
        else:
            dfpattern[" "] =  dfpattern[field].map(lambda x : 'Item compliant' if x == value else 'Not Item Compliant')
    
        dfpattern["Class"] = ["|"+str(val)+"|" for val in dfpattern["Class"]]

        fig = px.bar(dfpattern, x=targetAttribute, y="count", color=field, facet_col=" ")
        fig.update_layout(title={
            'text': field,
            'y':1.0,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'}, legend=dict(
            title=None, orientation="h", y=1.1, yanchor="bottom", x=0.5, xanchor="center"
        ))
        fig.write_html(str(pageNumber)+'.html', default_width='100%', default_height='100%')

    else:
        dfpattern = df

        if separador == "<=":
            dfpattern[" "] =  dfpattern[field].map(lambda x : 'Item compliant' if x <= float(value.replace(",",".")) else 'Not Item compliant')
            dfpattern[field] =  dfpattern[field].map(lambda x : pattern if x <= float(value.replace(",",".")) else opposite(pattern) )
            dfpattern = dfpattern.groupby([" " , field, targetAttribute]).size().reset_index().rename(columns={0:'count'})
        elif separador == "<":
            dfpattern[" "] =  dfpattern[field].map(lambda x : 'Item compliant' if x < float(value.replace(",",".")) else 'Not Item compliant' )
            dfpattern[field] =  dfpattern[field].map(lambda x : pattern if x < float(value.replace(",",".")) else opposite(pattern) )
            dfpattern = dfpattern.groupby([" " , field, targetAttribute]).size().reset_index().rename(columns={0:'count'})
        elif separador == ">=":
            dfpattern[" "] =  dfpattern[field].map(lambda x : 'Item compliant' if x >= float(value.replace(",",".")) else 'Not Item compliant' )
            dfpattern[field] =  dfpattern[field].map(lambda x : pattern if x >= float(value.replace(",",".")) else opposite(pattern) )
            dfpattern = dfpattern.groupby([" " , field, targetAttribute]).size().reset_index().rename(columns={0:'count'})
        else:
            dfpattern[" "] =  dfpattern[field].map(lambda x : 'Item compliant' if x > float(value.replace(",",".")) else 'Not Item compliant')
            dfpattern[field] =  dfpattern[field].map(lambda x : pattern if x > float(value.replace(",",".")) else opposite(pattern))
            dfpattern = dfpattern.groupby([" " , field, targetAttribute]).size().reset_index().rename(columns={0:'count'})
    
        dfpattern["Class"] = ["|"+str(val)+"|" for val in dfpattern["Class"]]

        fig = px.bar(dfpattern, x=targetAttribute, y="count", color=field, facet_col=" ")
        fig.update_layout(title={
            'text': field,
            'y':1.0,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'}, legend=dict(
            title=None, orientation="h", y=1.1, yanchor="bottom", x=0.5, xanchor="center"
        ))
        fig.write_html(str(pageNumber)+'.html', default_width='100%', default_height='100%')


doc = dominate.document(title='Pattern Visualization')

with doc.head:
    link(rel='stylesheet', href='style.css', type='text/css')
    script(src='https://code.jquery.com/jquery-3.5.1.js', integrity='sha256-QWo7LDvxbWT2tbbQ97B53yJnYU3WhH/C8ycbRAkjPDc=', crossorigin='anonymous')

with doc:
    h1('Pattern Visualization')
    h2('Pattern:')
    pre(originalPattern)
    with div():
        for i in range(patternSize):
            hr()
            h3('Item:')
            with div():
                pre(patternName[i], _class = "item")
            generatePatternPage(patternName[i], i, df, targetAttribute)
            iframe(src=str(i)+".html", onload="javascript:(function(o){o.style.height=o.contentWindow.document.body.scrollHeight+'px';}(this));", style="height:100%;width:70%;border:none;overflow:hidden;")

with open("index.html", "w", encoding='UTF-8') as document:
    document.write(str(doc).replace("<!DOCTYPE html>", ""))

with open("style.css", "w", encoding='UTF-8') as cssstyle:
    cssstyle.write("h1, h2, div { text-align: center; justify-content: center;} code { background: hsl(220, 80%, 90%); } pre { text-align: center; white-space: pre-wrap; background: hsl(30,80%,90%);} pre.item{width: 80%; margin-left: 10%; margin-right: 10%;}")

webbrowser.open_new_tab('index.html')