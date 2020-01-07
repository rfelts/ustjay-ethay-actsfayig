#!/usr/bin/env python3

# Russell Felts
# Pig Latin Assignment 05

""" You'll use the code to scrape a random fact from http://unkno.com (Links to an external site.)
and send it to a pig latin web application running on Heroku. """

import os

import requests
from flask import Flask, request, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """
    Get a random fact from unkno.com
    :return: String containing a random fact
    """
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


@app.route('/')
def home():
    """
    Create a seemingly random pig latin string
    :return: A Jinja2 template containing the URL of the pig latinized string
    """
    fact = {"input_text": get_fact()}
    response = requests.post("https://hidden-journey-62459.herokuapp.com/piglatinize/", data=fact,
                             allow_redirects=False)
    return render_template('base.jinja2', fact=fact.get("input_text"), pig_url=response.headers.get('Location'))


@app.route('/url')
def url():
    """
    Opens the requested URL
    :return: The content of the requested URL
    """
    response = requests.get(request.args.get('data'))
    return response.content


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
