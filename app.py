import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

# Set start date and today's date
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Streamlit app title and description
st.title('Smarter Shelves - Stock Prediction')
st.markdown("""
This app predicts future stock prices based on historical data. Select a stock ticker (e.g., 'RELIANCE.NS', 'AAPL') and specify the forecast period.
""")

# Sidebar for user inputs
st.sidebar.header('User Input Parameters')

# Let the user input any stock ticker
selected_stock = st.sidebar.text_input('Enter stock ticker (e.g., "RELIANCE.NS", "AAPL")')

# Input validation: Check if a ticker is provided
if not selected_stock:
    st.error("Please enter a stock ticker (e.g., 'RELIANCE.NS', 'AAPL').")

# Option for prediction years
n_years = st.sidebar.slider('Prediction years:', 1, 4)
period = n_years * 365  # Set forecast period to years in days

# Load stock data
@st.cache_data
def load_data(ticker):
    try:
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        if data.empty:
            st.error("No data found for the selected stock. Please choose a different stock.")
        return data
    except Exception as e:
        st.error(f"Error loading data for ticker {ticker}: {e}")
        return None

# Load data for the selected stock ticker
if selected_stock:
    data_load_state = st.text('Loading data...')
    data = load_data(selected_stock)
    data_load_state.text('Loading data... done!')

    # Data Overview and Forecasting
    if data is not None and len(data) > 1:
        # Display latest stock information
        st.subheader(f'{selected_stock} - Latest Data')
        st.write(f"**Latest Closing Price:** ${data['Close'].iloc[-1]:.2f}")
        st.write(f"**Volume:** {data['Volume'].iloc[-1]}")
        
        # Plot raw stock data (Open/Close prices)
        def plot_raw_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="Open Price"))
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close Price"))
            fig.layout.update(title_text=f'{selected_stock} Stock Price Over Time', xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)
        
        plot_raw_data()

        # Data preparation for forecasting (Prophet model)
        df_train = data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})
        m = Prophet()
        m.fit(df_train)

        # Make future predictions
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        # Display forecasted data
        st.subheader(f'Forecasted Data for {n_years} Year(s)')
        st.write(forecast.tail())
        
        # Predicted future stock insights
        st.subheader("Future Predictions Overview")
        forecast_period = forecast[(forecast['ds'] > TODAY)]
        avg_predicted_price = forecast_period['yhat'].mean()
        st.write(f"**Expected Average Price:** ${avg_predicted_price:.2f}")
        st.write(f"**Predicted High:** ${forecast_period['yhat_upper'].max():.2f}")
        st.write(f"**Predicted Low:** ${forecast_period['yhat_lower'].min():.2f}")

        # Plot forecasted data
        st.write(f'{selected_stock} Stock Price Forecast for {n_years} Year(s)')
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)

        # Display forecast components (trend, seasonality, etc.)
        st.write("Forecast Components")
        fig2 = m.plot_components(forecast)
        st.write(fig2)

    else:
        st.warning("Not enough data to perform forecasting. Please try again with a different stock or date range.")
