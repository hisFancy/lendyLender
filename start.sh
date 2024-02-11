#!/bin/bash

# Convert Jupyter notebook to HTML
jupyter nbconvert --to html --ExecutePreprocessor.timeout=-1 LendyLender.ipynb

# Start a simple web server to serve the HTML file
python -m http.server $PORT
