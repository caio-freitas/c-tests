from flask import Flask, request, render_template

app = Flask(__name__)
num_ans = 0
ans = []
title = ""
w = []

def html_gen(woerter, loesungen):
    erster_satz = ""
    i=0
    while i<len(woerter):
        
        wort = woerter[i]
        # erster Satz
        erster_satz += wort
        erster_satz += " "
        i+=1
        if '.' in wort:
            break
        
    #print(erster_satz)
    html_str = r"""
<!DOCTYPE html>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            
            <title>C-Test Generator: Im Ausland arbeiten</title>
            <link rel="stylesheet" type="text/css" href="./return_files/c-test.css">
            <script type="text/javascript"> 
            </script> 
        </head>

        <body class="vsc-initialized">
        <h5><strong>Ctest Instructions: Read the text and complete the blanked words.</strong></h5>
            <h3>{{title}}</h3>
                <form action="/ergebnis" method="POST">
                    <p class="ctest">
    """ + erster_satz
    j=1
    while i < len(woerter):
        #print(woerter[i])
        html_str += woerter[i] + '<input name="ctest{}" style="width: 12px;">'.format(j)
        i += 1
        j += 1
    html_str += "</p>"
    html_str += r"""
    <p class="ctest">Score: {{rchtg}}/{{nans}}</p>
                <p>&nbsp;</p>
                </p>
                <input type="submit" name="Ergebnis"> 
            </form> 
    """
    f = open("templates/test.html", "w")
    f.write(html_str)
    f.close()

def text_proc(raw):
    woerter = raw.split()
    test_woerter = []
    loesungen = []
    #print(woerter)
    # Ende des erstes Satzes finden
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
    return test_woerter, loesungen, ant_num
        

            

@app.route('/')
def input():
    return render_template('input.html')

@app.route('/', methods=['POST'])
def input_post():
    global num_ans, ans, w, title
    title = request.form['title']
    verarbeitet_title = title.title()
    raw_text = request.form['text']
    
    w, l , na = text_proc(raw_text)
    num_ans = na
    ans = l
    html_gen(w, l)
    page = render_template('test.html', title=title, main_text=w, nans=na, rchtg="____")
    return page

@app.route('/ergebnis', methods=['POST'])
def my_form_post():
    global num_ans, ans, w, title
    answers = []
    print(num_ans)
    richtige = 0
    berichte = ""
    for i in range(1, num_ans):
        
        answers.append(request.form['ctest{}'.format(i)])
        if request.form['ctest{}'.format(i)] == ans[i]:
            berichte += ("richtig: {}\n".format(ans[i]))
            richtige += 1
        else:
            berichte += ("falsch: {} != {}\n".format(request.form['ctest{}'.format(i)], ans[i]))
    req_data = request.get_json()
    print(answers)
    page = render_template('test.html', title=title, main_text=w, nans=num_ans, rchtg=richtige)
    
    return page