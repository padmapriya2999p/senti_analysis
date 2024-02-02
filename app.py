#inprogress not yet completed
# using flask 

from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

app=Flask(__name__)

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

@app.route('/')
@app.route('/home')
def home():
    form = UploadFileForm
    return'<h1>Sentiment Analysis</h1>'

if __name__=='__main__':
    app.run(debug=True)
