import requests
from twilio.rest import Client

# Load environment variables from the .env file
load_dotenv()

# Environment variables from the .env file
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
VIRTUAL_TWILIO_NUMBER = os.getenv("VIRTUAL_TWILIO_NUMBER")
VERIFIED_PHONE_NUMBER = os.getenv("VERIFIED_PHONE_NUMBER")
STOCK_NAME = os.getenv("STOCK_NAME")
COMPANY_NAME = os.getenv("COMPANY_NAME")

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
