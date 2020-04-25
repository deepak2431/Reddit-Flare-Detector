# Reddit Flair Detector

[![Python Version](https://img.shields.io/badge/python-3.7-brightgreen.svg)](https://python.org)


-----------------------------------------------------------------------------------------------------------------
**About the Project**

The project has been developed using the Reddit India Post datasets to predict the flair of any post using the URL of r/India posts. The data has been scrapped using the python PRAW library. The data scrapped has been preprocessed and clean further to build a machine learning model by trying out different algorithms and picking out the algorithm with the best accuracy.

The project has been deployed to heroku using the python Flask framework.

**Functionality:**
* Users can predict the flair of any Reddit India posts by submitting the URL of the post.

This application is deployed on heroku. To checkout this application visit this link https://redditflairdetector20.herokuapp.com/

**Project Structure**
* The project contains two directory:
1. model_files: This directory contains all the jupyter notebooks code used for scrapping the data, cleaning the data, and the machine learning model code.
2. website_files: This directort contains the script used to build the web application using the Machine Learning model.

**To setup the project on your local machine:**

1. Click on `Fork`.
2. Go to your fork and `clone` the project to your local machine.
3. Create a virtual environment `python -m venv venv`.
4. Activate the virtual environment `source venv\bin\activate`.
5. After activating the virtual environment move to the project folder using cd command.
6. Move to the `website` directory.
7. Install all the dependencies using `pip install -r requirements.txt`.
8. Export the flask script using `export FLASK_APP=script.py`.
9. Run the server using `flask run`.

The project will be available at **127.0.0.1:5000**.


**To contribute to the project:**

1. Choose any open issue from.
2. Comment on the issue: `Can I work on this?` and get assigned.
3. Make changes to your fork and send a PR.

**To create a PR:**

Follow the given link to make a successful and valid PR: https://help.github.com/articles/creating-a-pull-request/

**To send a PR, follow these rules carefully,**otherwise your PR will be closed**:**

1. Make PR title in this format: `Fixes #IssueNo : Name of Issue`

For any doubts related to the issues, i.e., to understand the issue better etc, comment down your queries on the respective issue.



