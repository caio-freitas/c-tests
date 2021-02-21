from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my_form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    title = request.form['title']
    processed_title = title.title()
    processed_text = request.form['text']
    
    return processed_text