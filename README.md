# Sentiment-Analysis-with-CamemBERT-model

# Trustpilot Sentiment Analysis

This project contains a script that performs a sentiment prediction over the comments found on the website fr.trustpilot.com. Sentiment prediction displays two different outputs, positive :) or negative :( regarding the general feeling of the phrases and comments posted by users regarding their satisfaction over the service offered by the companies on the website.  The comments mining over the website is done based on two criteria: the business category and the geographic location by zip code 

## Dependencies

Following dependencies are required in order to run the project:

### Libraries

pip freeze > requirements.txt
spacy==3.0.5 → pip3 install spacy
tensorflow==2.4.1 → pip3 install tensorflow
transformers==4.4.2 → pip3 install transformers
pandas==1.2.2 → pip3 install pandas
numpy==1.20.1 → pip3 install numpy
requests==2.22.0 → pip3 install requests
torch==1.8.0 → pip3 install torch
emoji==1.2.0 → pip3 install emoji
nltk==3.5 → pip3 install nltk
Keras==2.4.3 → pip3 install Keras
wordcloud==1.8.1 → pip3 install wordcloud
beautifulsoup4==4.9.3 → pip3 install beautifulsoup4
fastapi==0.63.0 → pip3 install fastapi


### Files python

*model_camembert_training_googlecolab
It contains the code necessary to scrap fr.trustpilot.com and train the model in order to download model weight for furthers predictions

* scraping_Trustpilot

It contains three functions: the first one serves to scrap the name of the company regarding the category.The second one serves to scrap the comments of companies regarding the category. The third one serves the comments of companies regarding the category and its zip code.

* word_cloud

Word Cloud is a data visualization technique used for representing text data in which the size of each word indicates its frequency or importance. Significant textual data points can be highlighted using a word cloud. Word clouds are widely used for analyzing data from social network websites.


*  data_eng

It serves to preprocess the data using four processes: remove punctuation marks, remove the so called “stop word”, applying the steaming and finally the lemmatizing. 

*  model_camemBERT

It is a model nlp based roBERTa architecture for french language used to perform sentiment prediction. We chose this model for our API because it is the most popular and easy to use and has a large support community.
The model was trained on Google colab and the resulting model weight (sentiment.pt) was downloaded into our project to avoid larger calculation times.


## Hardware requirements

* at least **8 GB** of RAM

Tested on Ubuntu 20.04 with no GPU


Our team's name is **Group 4**.

Here is the link for our presentation : Group 4 Sentiment Analysis API Presentation
https://docs.google.com/presentation/d/1MT59BI7QEeYUdzuIhP5iYq-oCfEnV2-9b7C89I-H72U/edit#slide=id.gca34e2ae8e_0_0

Team members:

* Maya SAFA 
* Khaled SAAD 
* Diego MAGALDI 


To launch the trained model for sentiment prediction using fastapi, from the terminal use the line: 
uvicorn api:app --reload
Then to perform the sentiment analysis, from the browser on a local server using two arguments, company category and zip code as:
http://127.0.0.1:8000/predict/{company’s category}/{zip code}/ . 
Example:  
http://127.0.0.1:8000/predict/shopping_fashion/0 (for company’s category, shopping_fashion and zip code, 
http://127.0.0.1:8000/predict/shopping_fashion/75/
 for a general search by adding the first two numbers of the zip code example: 75 for whole Paris area) 


Using the local path ‘data/sentiment.pt’ directory where the stored weight for the CamemBERT model 



