"""A Streamlit app for getting the Google autocomplete queries
"""
import json
import requests
import streamlit as st
#import streamlit_authenticator as stauth
import yaml
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import warnings
warnings.filterwarnings('ignore')
# function to print sentiments
# of the sentence.
def sentiment_scores(sentence):

	# Create a SentimentIntensityAnalyzer object.
	sid_obj = SentimentIntensityAnalyzer()

	# polarity_scores method of SentimentIntensityAnalyzer
	# object gives a sentiment dictionary.
	# which contains pos, neg, neu, and compound scores.
	sentiment_dict = sid_obj.polarity_scores(sentence)
	
	#print("Overall sentiment dictionary is : ", sentiment_dict)
	#print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
	#print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
	#print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")

	print("Sentence Overall Rated As", end = " ")
	sent=""
	# decide sentiment as positive, negative and neutral
	if sentiment_dict['compound'] >= 0.05 :
		sent="Positive"
		print("Positive")

	elif sentiment_dict['compound'] <= - 0.05 :
		sent="Negative"
		print("Negative")

	else :
		sent="Neutral"
		print("Neutral")
	return sent





# The Streamlit app
st.set_page_config(
    page_title="Query Engine!",
    page_icon="😎",
    layout="wide"
)

# The Streamlit app authentication section
with open("./config.yaml") as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

#authenticator = stauth.Authenticate(
#   config["credentials"],
#    config["cookie"]["name"],
#    config["cookie"]["key"],
#   config["cookie"]["expiry_days"],
#    config["preauthorized"]
#)

#name, authentication_status, username = authenticator.login("Login", "main")

#if authentication_status:
#   authenticator.logout('Logout', 'main')

#    # The Streamlit app main section
st.title("Sentiment Analysis!!!")
#st.write("Make your ideas real.")
output=""
sentence: str = st.text_input("Enter a text and Press Enter key")
st.write("Or")
uploaded_file = st.file_uploader("Upload a CSV file after entering sentences under a column named Query")
if sentence:
    output = sentiment_scores(sentence)
if output:
    st.header(output)

if uploaded_file is not None:
    #read csv
    df=pd.read_csv(uploaded_file,encoding='cp1252',engine='python')
else:
    st.warning("you need to upload a csv file")
if uploaded_file:
    senti_list=[]
    df_results=pd.DataFrame()
    for index,row in df.iterrows():
        sentence=row['Query']
		# function calling
        sentiment=sentiment_scores(sentence)
        senti_list.append(sentiment)
    df_results['Question']=df['Query']
    df_results['Results']=senti_list
    csv=df_results.to_csv(index=False).encode('utf-8')
    #if output_list_google_autocomplete:
    st.download_button("Download the output",
                       csv,"Sentiment Results.csv","text/csv",key='download-csv')

#elif not authentication_status:
#    st.error('Username/password is incorrect')
#elif authentication_status is None:
#    st.warning('Please enter your username and password')
