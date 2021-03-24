import torch
import numpy
import numpy as np
import os
import json
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences
from transformers import CamembertForSequenceClassification, CamembertTokenizer, \
                         AdamW, get_linear_schedule_with_warmup

from scraping_Truspilot import scraping_trustpilot_category
from data_eng import remove_stop_words

# Defining constants
epochs = 5
MAX_LEN = 128
batch_size = 1
device = torch.device('cpu')


# Initialize CamemBERT tokenizer
tokenizer = CamembertTokenizer.from_pretrained('camembert-base',do_lower_case=True)

model = CamembertForSequenceClassification.from_pretrained("camembert-base", num_labels=2)
model.to(device)

model.load_state_dict(torch.load('/home/txolo/Documents/API/Group4/data/sentiments.pt', map_location=torch.device('cpu')))

def model_camemBERT_predict(category: str, comments: list):

    sentiments_positive = []
    list_comments_positive = []
    sentiments_negative = []
    list_comments_negative = []

    # Encode the comments
    tokenized_comments_ids = [tokenizer.encode(comment,add_special_tokens=True,max_length=MAX_LEN) for comment in comments]
    # Pad the resulted encoded comments
    tokenized_comments_ids = pad_sequences(tokenized_comments_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")

    # Create attention masks 
    attention_masks = []
    for seq in tokenized_comments_ids:
        seq_mask = [float(i>0) for i in seq]
        attention_masks.append(seq_mask)

    prediction_inputs = torch.tensor(tokenized_comments_ids)
    prediction_masks = torch.tensor(attention_masks)

    # Apply the finetuned model (Camembert)
    flat_pred = []
    with torch.no_grad():
        # Forward pass, calculate logit predictions
        outputs =  model(prediction_inputs.to(device),token_type_ids=None, attention_mask=prediction_masks.to(device))
        logits = outputs[0]
        logits = logits.detach().cpu().numpy() 
        flat_pred.extend(np.argmax(logits, axis=1).flatten())



    Dict_prediction = dict()
    for i in range(len(flat_pred)):
        
        Dict_prediction[str(comments[i])] = int(flat_pred[i])
    
    for k in Dict_prediction.keys():
        if Dict_prediction[k] == 1:
            sentiments_positive.append(1)
            list_comments_positive.append(remove_stop_words(k))
        elif Dict_prediction[k] == 0:
            sentiments_negative.append(0)
            list_comments_negative.append(remove_stop_words(k))


    
    json_dump = json.dumps(Dict_prediction, indent = 4)


    return sentiments_positive, sentiments_negative, list_comments_positive, list_comments_negative 