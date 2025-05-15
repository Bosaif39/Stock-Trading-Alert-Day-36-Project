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

## STEP 1: Get stock data and compare price changes.
# Fetch yesterday's closing stock price using the Alpha Vantage API.

stock_params = {
    "function": "TIME_SERIES_DAILY",  # We're using the daily time series function to get daily stock prices
    "symbol": STOCK_NAME,  # The stock ticker symbol (e.g., TSLA for Tesla)
    "apikey": STOCK_API_KEY,  # Your Alpha Vantage API key
}

# Send a GET request to the Alpha Vantage API
response = requests.get(STOCK_ENDPOINT, params=stock_params)

# Convert the API response to a dictionary and extract daily stock data
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]  # Convert the data into a list for easier manipulation

# Get the stock price for yesterday (most recent available)
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]  # '4. close' is the closing price field
print(yesterday_closing_price)  # Print yesterday's closing price

# Get the stock price for the day before yesterday (second most recent)
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)  # Print the day before yesterday's closing price

# STEP 1 continued: Calculate the price difference and determine the price movement
# Find the absolute difference between the two closing prices
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

# Determine whether the price went up or down
up_down = None
if difference > 0:
    up_down = "🔺"  # Price went up
else:
    up_down = "🔻"  # Price went down

# Calculate the percentage change in price between the two days
diff_percent = round((difference / float(yesterday_closing_price)) * 100)  # Round to the nearest whole number
print(diff_percent)  # Print the percentage change

## STEP 2: Get news related to the company if the stock price change is greater than 1%
# If the stock price change is greater than 1% in either direction, fetch news articles
if abs(diff_percent) > 1:
    # Set up the parameters for fetching news articles from the News API
    news_params = {
        "apiKey": NEWS_API_KEY,  # Your News API key
        "qInTitle": COMPANY_NAME,  # Search for news articles with the company name in the title
    }

    # Send a GET request to the News API to get the latest articles
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]  # Extract the articles from the response

    # Get the first 3 articles from the response using Python's slicing
    three_articles = articles[:3]
    print(three_articles)  # Print the list of articles (for debugging)

## STEP 3: Format articles and send them via Twilio SMS
# Format the first 3 articles into a list of strings with the stock movement and article details
formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
print(formatted_articles)  # Print the formatted articles (for debugging)

# Send the formatted articles as separate messages via Twilio
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)  # Initialize the Twilio client with your SID and auth token

# Loop through each formatted article and send it as an SMS
for article in formatted_articles:
    message = client.messages.create(
        body=article,  # The message body contains the formatted article
        from_=VIRTUAL_TWILIO_NUMBER,  # The Twilio number from which the SMS will be sent
        to=VERIFIED_NUMBER  # Your verified phone number to receive the SMS
    )
