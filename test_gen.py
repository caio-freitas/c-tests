from flask import Flask, request, render_template

app = Flask(__name__)


def text_proc(raw):
    woerter = raw.split()
    test_woerter = []
    loesungen = []
    print(woerter)
    # Ende des erstes Satzes zu finden
    i=0
    erster=True
    geradzahlig=True
    ant_num = 0
    while i<len(woerter):
        wort = woerter[i]
        # erster Satz
        if erster:
            test_woerter.append(wort)
            if '.' not in wort:
                pass
            else:
                erster=False

        else:
            if geradzahlig or len(wort)<3:
                test_woerter.append(wort)
            else:
                if len(wort)>3:
                    test_woerter.append(wort[:len(wort)-3])
                    loesungen.append(wort[len(wort)-3:])
                    ant_num+=1
            geradzahlig = not geradzahlig #abwechseln
        i += 1

    test_text = ""
    for wort in test_woerter:
        test_text += wort
        test_text += " "
    return test_text, loesungen, ant_num
        

            

@app.route('/')
def input():
    return render_template('input.html')

@app.route('/', methods=['POST'])
def input_post():
    title = request.form['title']
    verarbeitet_title = title.title()
    raw_text = request.form['text']
    
    w, l , na= text_proc(raw_text)
    
    page = render_template('return.html', title=title, main_text=w, nans=na)
    return page

@app.route('/', methods=['POST'])
def my_form_post():
    title = request.form['title']
    verarbeitet_title = title.title()
    verarbeitet_text = request.form['text']
    
    return verarbeitet_text