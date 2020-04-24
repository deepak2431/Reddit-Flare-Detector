#importing libraries
import os
import numpy as np
import flask
import pickle
import praw
import json
import textcleaning as cleanTxt
from flask import Flask, render_template, request, url_for, send_from_directory, redirect, jsonify
from werkzeug.utils import secure_filename
from werkzeug.middleware.shared_data import SharedDataMiddleware

UPLOAD_FOLDER = 'uploaded_files'
DOWNLOAD_FOLDER = 'download_files'
ALLOWED_EXTENSIONS = {'txt'}

reddit = praw.Reddit(client_id='EU0x1aDplXDqDA', \
                     client_secret='B7UQzWrWB5C0sOfI0PcN9UXh6tE', \
                     user_agent='flare_detector', \
                     username='deepakdk2431', \
                     password='Deepakdk#6422')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_endpoint_url(url):

    result = []

    submission = reddit.submission(url = url)
    data = {}
    data["title"] = str(submission.title)
    data["url"] = str(submission.url)
    data["body"] = str(submission.selftext)
    
    submission.comments.replace_more(limit=None)
    comment = ''
    count = 0
    for top_level_comment in submission.comments:
        comment = comment + ' ' + top_level_comment.body
        count+=1
        if(count > 20):
            break
    
    data["comment"] = str(comment)
    data['title'] = cleanTxt.clean_text(str(data['title']))
    data['body'] = cleanTxt.clean_text(str(data['body']))
    data['comment'] = cleanTxt.clean_text(str(data['comment']))

    combined_features = data["title"] + data["comment"] + data["body"] + data["url"]
    
    model = pickle.load(open('sgdClf.pkl','rb'))
    flair_prediction = model.predict([combined_features])

    return flair_prediction



def prediction(url):

    result = []

    submission = reddit.submission(url = url)
    data = {}
    data["title"] = str(submission.title)
    data["url"] = str(submission.url)
    data["body"] = str(submission.selftext)
    
    submission.comments.replace_more(limit=None)
    comment = ''
    count = 0
    for top_level_comment in submission.comments:
        comment = comment + ' ' + top_level_comment.body
        count+=1
        if(count > 20):
            break
    
    data["comment"] = str(comment)
    data['title'] = cleanTxt.clean_text(str(data['title']))
    data['body'] = cleanTxt.clean_text(str(data['body']))
    data['comment'] = cleanTxt.clean_text(str(data['comment']))

    result.append(data["title"])
    result.append(data["url"])
    result.append(data["body"])


    
    combined_features = data["title"] + data["comment"] + data["body"] + data["url"]
    
    model = pickle.load(open('sgdClf.pkl','rb'))
    model_prediction = model.predict([combined_features])

    result.append(model_prediction)    
    return result

#creating instance of the class
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

#to tell flask what url shoud trigger the function home()
@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():

    if request.method == 'GET':
        return flask.render_template('index.html')

    if request.method == 'POST':
        text = flask.request.form['url']
        
        flair_prediction = prediction(str(text))
    
        return flask.render_template('layout.html', result=flair_prediction)


'''@app.route('/uploads/<filename>')
def uploaded_file(filename):

    file_content = send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    return flask.render_template('form_get.html', filedata=file_content)'''

@app.route('/content/<filename>')
def content(filename):
    
    
    flair_list = []
    text = open(filename, 'r+')
    file_data = text.readlines()

    for urls in file_data:
        predicted_flair = predict_endpoint_url(urls)
        flair_list.append(predicted_flair)

    result_dic = dict(zip(file_data, flair_list))
    text.close()

    return flask.render_template('form_post.html', predicted_flair=result_dic)


@app.route('/endpoints', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return redirect(url_for('content',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == 'main':
    app.run(debug=True)
