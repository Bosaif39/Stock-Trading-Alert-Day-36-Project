
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
pip install python-dotenv
```

* **requests**: This library helps you make HTTP requests to external APIs.
* **twilio**: This library allows you to interact with the Twilio service to send SMS notifications.
* **python-dotenv**: This package allows you to load environment variables from the `.env` file.

### **3. Update the Script**

Here is the script you'll be using to track the stock price and send SMS alerts:

```python
import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

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

# Alpha Vantage API endpoint for stock data
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
# News API endpoint for news data
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Step 1: Fetch the stock data (closing prices)
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_data = stock_response.json()["Time Series (Daily)"]
data_list = [value for key, value in stock_data.items()]

# Get the stock prices for yesterday and the day before
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

# Calculate the price difference and percentage change
price_difference = yesterday_closing_price - day_before_yesterday_closing_price
percentage_change = round((price_difference / day_before_yesterday_closing_price) * 100)

# Step 2: Check if the percentage change is greater than 5% (up or down)
if abs(percentage_change) > 5:
    # Get the latest news about the company from NewsAPI
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_articles = news_response.json()["articles"][:3]

    # Format the articles for SMS
    formatted_articles = [
        f"{STOCK_NAME}: {'🔺' if percentage_change > 0 else '🔻'}{abs(percentage_change)}%\n"
        f"Headline: {article['title']}\nBrief: {article['description']}" 
        for article in news_articles
    ]

    # Step 3: Send each article as a separate SMS using Twilio
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_PHONE_NUMBER
        )
```

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
* **python-dotenv**: Install with `pip install python-dotenv`.

## **Troubleshooting**

* **Missing API Key**: If you encounter an error related to the API key, double-check that you've entered your keys correctly in the `.env` file.
* **No SMS**: If you aren't receiving SMS, verify that your Twilio account is set up correctly and that you've added your verified phone number.

