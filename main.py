import requests
from twilio.rest import Client

# Your Twilio virtual phone number and the verified phone number
VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
VERIFIED_NUMBER = "your own phone number verified with Twilio"

# The stock symbol and the company name you're tracking
STOCK_NAME = "MSFT"
COMPANY_NAME = "Microsoft"

# Alpha Vantage and News API endpoints for stock and news data
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# API keys for Alpha Vantage and News API, as well as Twilio credentials
STOCK_API_KEY = "YOUR OWN API KEY FROM ALPHAVANTAGE"
NEWS_API_KEY = "YOUR OWN API KEY FROM NEWSAPI"
TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

# Fetch yesterday's closing stock price using the Alpha Vantage API.
stock_params = {
    "function": "TIME_SERIES_DAILY",  
    "symbol": STOCK_NAME,  
    "apikey": STOCK_API_KEY,  
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()

data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]  # Convert the data into a list for easier manipulation

# Get the stock price for yesterday (most recent available)
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]  
print(yesterday_closing_price)  

# Get the stock price for the day before yesterday (second most recent)
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)  

# Find the absolute difference between the two closing prices
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
difference = abs(difference)

# Determine whether the price went up or down
up_down = None
if difference > 5:
    up_down = "🔺"  
else:
    up_down = "🔻"  

# Calculate the percentage change in price between the two days
diff_percent = round((difference / float(yesterday_closing_price)) * 100)  
print(diff_percent)  

# If the stock price change is greater than 5% in either direction, fetch news articles
if abs(diff_percent) > 5:

    news_params = {
        "apiKey": NEWS_API_KEY,  
        "qInTitle": COMPANY_NAME,  
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]  # Extract the articles from the response

    # Get the first 3 articles from the response using Python's slicing
    three_articles = articles[:3]
    print(three_articles)  

# Format the first 3 articles into a list of strings with the stock movement and article details
formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
print(formatted_articles)  

# Send the formatted articles as separate messages via Twilio
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)  

# Loop through each formatted article and send it as an SMS
for article in formatted_articles:
    message = client.messages.create(
        body=article,  
        from_=VIRTUAL_TWILIO_NUMBER,  
        to=VERIFIED_NUMBER  
    )
