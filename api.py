import numpy
import numpy as np
import os
import json


from typing import Optional
from fastapi import FastAPI
from scraping_Truspilot import scraping_trustpilot_category, scraping_trustpilot_with_zip_code
from model_camemBERT import model_camemBERT_predict
from word_cloud import wordcloud_generate

app = FastAPI() 


@app.get("/")
def read_root():
    return " Welcome to API for sentiment analysis using camembert Model for french language to predict the sentiment from trustpilot site"



@app.get("/predict/{catg}/{zip_postal}")
def root_model(catg: str, zip_postal: Optional[int]= 0):  

    Dict_json = dict()
    Dict_json["The_comments"] = dict()
    Dict_json["world_cloud"] = dict()
    
    if zip_postal == 0:
        list_of_companies, comments = scraping_trustpilot_category(catg)
    else:
        list_of_companies, comments = scraping_trustpilot_with_zip_code(catg, zip_postal)

    Dict_json["number_of_company"] = len(list_of_companies)
    Dict_json["number_of_comments"] = len(comments)

    p, n, cp, cn = model_camemBERT_predict(catg, comments)
    Dict_json["The_comments"]["positive"] = len(p)
    Dict_json["The_comments"]["negative"] = len(n)

    Dict_json["world_cloud"]["positive"] = wordcloud_generate(cp)
    Dict_json["world_cloud"]["negative"] = wordcloud_generate(cn)

    json_dump = json.dumps(Dict_json, indent = 4, ensure_ascii = False)

    
    with open("/home/txolo/Documents/API/Group4/data/sample.json", "w") as outfile:
        outfile.write(json_dump)

    return json_dump
