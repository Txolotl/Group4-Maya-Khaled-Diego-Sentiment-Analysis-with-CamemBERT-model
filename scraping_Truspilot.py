import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import emoji
from data_eng import clean_txt, remove_stop_words, return_stem, lemmat


Dict_category = dict()


def list_category(category_name: str)-> dict:  # /reviews/{name of company}
  pages = np.arange(1, 100, 1)

  for page in pages:
    url = "https://fr.trustpilot.com/categories/"+ category_name + "?page=" + str(page)
    page_html = requests.get(url)

    if(page_html.url != url): # redirect occurred; likely symbol doesn't exist or cannot be found.
      raise requests.TooManyRedirects()

    page_html.raise_for_status()

    soup = BeautifulSoup(page_html.text, "html.parser")

    find_pages = soup.find_all('a', class_="link_internal__YpiJI link_wrapper__LEdx5")

    ## path link for each company
    for val in find_pages:
      Dict_company = dict()
      ln = val.get('href')
      if str(ln).startswith('/review'):

        ## name of company
        name = val.find_all('div', class_="styles_businessTitle__1IANo")
        if len(name) != 0:
          n = str(name[0]).split('1IANo">')
          name_company = n[1].split('</')[0]
          Dict_company['name_company'] = name_company

        ## code postal
        zip = val.find_all('span', class_="styles_locationZipcodeAndCity__2RbYT")

        if len(zip) != 0:
          z = str(zip[0]).split('<span>')
          code_postal = z[1].split('<')[0]
          Dict_company['code_postale'] = code_postal
        else:
          Dict_company['code_postale'] = 0


        ## number of reviews
        score = val.find_all('div', class_="styles_textRating__19_fv")
        if len(score) != 0:
          s = str(score[0]).split('fv">')
          number_reviews = s[1].split('avis')[0]
          Dict_company['number_reviews'] = number_reviews
          
          ## score number
          t = str(score[0]).split('TrustScore')
          trust_score = t[1].split('</')[0]
          Dict_company['score'] = trust_score
        else:
          Dict_company['number_reviews'] = 0
          Dict_company['score'] = 0

        Dict_category[ln] = Dict_company

    return Dict_category


## ********************************************* category without zip code **********************************************************


def scraping_trustpilot_category(category: str):
  acount_c = []
  merge_title_body = []
  reviewers_c = []
  dates_c = []
  stars_c = []
  headings_c = []
  reviews_c = []
  name_companies_c = []
  acount_c.append(category)
  Dic = list_category(category)
  for key in list(Dic.keys()):
    name_companies_c.append(Dic[key]['name_company']) 
    
    #Set number of pages to scrape
    pages = np.arange(1, 100, 1)

    #Create a loop to go over the reviews
    for page in pages:
        url = "https://fr.trustpilot.com/" + key + "?page=" + str(page)

        page_html = requests.get(url)

        soup = BeautifulSoup(page_html.text, "html.parser")
        #Set the tag we wish to start at
        review_div = soup.find_all('article', class_="review")
        review_div1 = soup.find_all('div', class_="review-content")

            #loop to iterate through each reviews
        for container in review_div:

            #Get reviewer
            nv = container.find_all('div', attrs={'class': 'consumer-information__name'})
            reviewer = container.div.text if len(nv) == True else '-'
            reviewers_c.append(reviewer)

        for container in review_div1:

            #Get the body of the review
            nv = container.find_all('p', attrs={'class': 'review-content__text'})
            review = container.p.text if len(nv) == True else '-'
            reviews_c.append(review)

            #Get the title of the review
            nv1 = container.find_all('h2', attrs={'class': 'review-content__title'})
            heading = container.a.text if len(nv1) == True else '-'
            headings_c.append(heading)

            #Get the star rating review given
            star = container.find("div", {"class":"star-rating star-rating--medium"}).find('img').get('alt')
            stars_c.append(star)

            #Get the date
            date_json = json.loads(container.find('script').string)
            date = date_json['publishedDate']
            dates_c.append(date)

            #merge title and body
            merge = review.strip() + ' ' + heading.strip()
            emj = emoji.demojize(merge)
            clean = clean_txt(emj)
            remove = remove_stop_words(clean)
            # stm = return_stem(remove)
            # lemis = lemmat(stm)
            merge_title_body.append(remove)


  return name_companies_c, merge_title_body



## ******************************************************** category with zip code **********************************************************


def scraping_trustpilot_with_zip_code(category: str, zip_code: int):
  merge_title_body_zipcode = []
  acount = []
  reviewers = []
  dates = []
  stars = []
  headings = []
  reviews = []
  name_companies = []
  code_postale = []

  acount.append(category)
  Dic = list_category(category)

  for key in list(Dic.keys()):

    if str(Dic[key]['code_postale']).startswith(str(zip_code)):
      code_postale.append(Dic[key]['code_postale'])
      name_companies.append(Dic[key]['name_company']) 

      #Set number of pages to scrape
      pages = np.arange(1, 100, 1)

      #Create a loop to go over the reviews
      for page in pages:
        url1 = "https://fr.trustpilot.com/" + key + "?page=" + str(page)

        page_html = requests.get(url1)

        
        soup = BeautifulSoup(page_html.text, "html.parser")
        #Set the tag we wish to start at
        review_div = soup.find_all('article', class_="review")
        review_div1 = soup.find_all('div', class_="review-content")

            #loop to iterate through each reviews
        for container in review_div:

            #Get reviewer
            nv = container.find_all('div', attrs={'class': 'consumer-information__name'})
            reviewer = container.div.text if len(nv) == True else '-'
            reviewers.append(reviewer)

        for container in review_div1:

            #Get the body of the review
            nv = container.find_all('p', attrs={'class': 'review-content__text'})
            review1 = container.p.text if len(nv) == True else '-'
            reviews.append(review1)

            #Get the title of the review
            nv1 = container.find_all('h2', attrs={'class': 'review-content__title'})
            heading1 = container.a.text if len(nv1) == True else '-'
            headings.append(heading1)

            #Get the star rating review given
            star = container.find("div", {"class":"star-rating star-rating--medium"}).find('img').get('alt')
            stars.append(star)

            #Get the date
            date_json = json.loads(container.find('script').string)
            date = date_json['publishedDate']
            dates.append(date)

            #merge title and body
            merge1 = review1.strip() + ' ' + heading1.strip()
            emj1 = emoji.demojize(merge1)
            clean1 = clean_txt(emj1)
            remove1 = remove_stop_words(clean1)
            # stm1 = return_stem(remove1)
            # lemis1 = lemmat(stm1)
            merge_title_body_zipcode.append(remove1)
    else:
      continue

  return name_companies, merge_title_body_zipcode
