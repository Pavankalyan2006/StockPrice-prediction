pip install streamlit yfinance prophet plotly pandas numpy



teps to Run Your Streamlit Stock Prediction App:
1. Install Required Packages (if not installed)
Run the following command in your terminal or command prompt:

sh
Copy
Edit
pip install streamlit yfinance prophet plotly pandas numpy
2. Save Your Code
Save your Python script as app.py.

3. Run the Streamlit App
Navigate to the folder where app.py is located using the terminal or command prompt. Then, run:

sh
Copy
Edit
streamlit run app.py
4. Open the Web App
After running the above command, Streamlit will start a local server, and you'll see an output like:

arduino
Copy
Edit
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://your-ip:8501
Click on the Local URL (e.g., http://localhost:8501) to open the app in your browser.

5. Enter Stock Ticker and Forecast Period
Input a stock ticker like AAPL (for Apple) or RELIANCE.NS (for Reliance India).
Select the number of years for the prediction.
The app will display stock prices, trends, and forecasts.
🔹 Troubleshooting:

If you get a ModuleNotFoundError, ensure all required packages are installed.
If prophet fails to install, try:
sh
Copy
Edit
pip install cmdstanpy
