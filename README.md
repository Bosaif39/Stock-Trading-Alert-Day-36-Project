
# **Stock Trading Alert**

## **Overview**

This is the Day 36 project from the **"100 Days of Code: The Complete Python Pro Bootcamp"**.

This project aims to monitor the stock price of a company and send SMS alerts when significant changes (e.g., a 5% increase or decrease) are detected. The script uses the Alpha Vantage API to fetch stock data, the News API to retrieve related news articles, and Twilio to send SMS notifications.

## **How It Works**

1. **Fetch Stock Data**: The script queries the Alpha Vantage API to retrieve the latest stock prices (closing prices for two consecutive days).
2. **Detect Price Change**: It calculates the percentage change between the two stock closing prices.
3. **Trigger Alerts**: If the stock price changes by more than 5%, it triggers the News API to fetch the latest articles about the company.
4. **Send SMS Notifications**: The script formats the news articles and sends them as SMS alerts to your phone via Twilio.

## **Instructions**

### **1. Set Up Environment Variables**

In this step, you'll store sensitive information (API keys and Twilio credentials) securely.

#### a. **Create a `.env` File:**

* Create a file named `.env` in the same directory as the script.
* This file will store your API keys and Twilio account details to keep them safe.

#### b. **Add Your API Keys and Configuration:**

Open the `.env` file and add the following variables. Replace the placeholder text with your actual credentials.

```bash
STOCK_API_KEY=your_alpha_vantage_api_key
NEWS_API_KEY=your_news_api_key
TWILIO_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
VIRTUAL_TWILIO_NUMBER=your_twilio_virtual_number
VERIFIED_PHONE_NUMBER=your_verified_phone_number
STOCK_NAME=the_stock_symbol_to_track (e.g., TSLA)
COMPANY_NAME=company_name_to_fetch_news_for 
```

* **STOCK\_API\_KEY**: Your API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).
* **NEWS\_API\_KEY**: Your API key from [NewsAPI](https://newsapi.org/).
* **TWILIO\_SID**: Your Account SID from [Twilio](https://www.twilio.com/).
* **TWILIO\_AUTH\_TOKEN**: Your Auth Token from Twilio.
* **VIRTUAL\_TWILIO\_NUMBER**: Your Twilio virtual phone number from which messages will be sent.
* **VERIFIED\_PHONE\_NUMBER**: Your verified phone number to receive the SMS alerts.
* **STOCK\_NAME**: The stock symbol you want to track.
* **COMPANY\_NAME**: The name of the company for which you want to fetch news.

### **2. Install Dependencies**

You need to install some Python libraries to run the script.

* Open a terminal or command prompt and navigate to your project directory.
* Install the required libraries by running the following commands:

```bash
pip install requests
pip install twilio
```

* **requests**: This library helps you make HTTP requests to external APIs.
* **twilio**: This library allows you to interact with the Twilio service to send SMS notifications.

### **3. Update the Script**

Here is the script you'll be using to track the stock price and send SMS alerts:

```python
import requests
from twilio.rest import Client

# Environment variables from the .env file
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
VIRTUAL_TWILIO_NUMBER = os.environ.get("VIRTUAL_TWILIO_NUMBER")
VERIFIED_PHONE_NUMBER = os.environ.get("VERIFIED_PHONE_NUMBER")
STOCK_NAME = os.environ.get("STOCK_NAME")
COMPANY_NAME = os.environ.get("COMPANY_NAME")

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
    )```

### **4. Run the Script**

Once the script is set up and you have configured the `.env` file with your keys and values, you can run the script from your terminal.

* Navigate to the directory where your script is located.
* Run the script using the following command:

```bash
python stock_trading_alert.py
```

If everything is configured correctly, you'll receive SMS alerts if the stock price changes by more than 5%. The alert will contain news headlines and brief descriptions related to the company.

## **Requirements**

* **Python 3.x**: This script requires Python 3 or later.
* **Requests**: Install with `pip install requests`.
* **Twilio**: Install with `pip install twilio`.
