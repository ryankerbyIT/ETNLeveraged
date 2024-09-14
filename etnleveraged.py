# -------------------------------------------------------------
# Investment Backtest Tool: Comprehensive Documentation
# -------------------------------------------------------------

# 1. Overview
# The Investment Backtest Tool is a Python-based GUI application 
# that allows users to backtest the performance of stock investments 
# over time. It uses yfinance to fetch historical stock data, 
# calculates the investment value based on a user-defined start 
# and end date (2009 to 2024), and visualizes the stock performance 
# using mplfinance. The tool allows users to input a stock ticker 
# and displays the results in an interactive GUI.

# Key Features:
# - Input any valid ticker symbol to backtest stock performance.
# - Visualize stock price performance in a line chart.
# - Calculate the value of an initial investment of $10,000.
# - Zoom text in the result box with a dynamic slider.
# - Draggable result text box for flexibility.
# - Error handling for invalid or empty stock data.

# -------------------------------------------------------------

# 2. Application Structure

# 2.1 Libraries Used
# - pandas: For data handling and resampling.
# - yfinance: To fetch historical stock data.
# - mplfinance: To plot stock performance.
# - tkinter: For creating the graphical user interface (GUI).
# - matplotlib: To render charts inside tkinter.
# - simpledialog: For input dialog box.

# 2.2 Main Components

# 2.2.1 Data Fetching and Investment Calculation
# The fetch_data function retrieves the historical stock data using 
# the ticker symbol, start date, and end date. The 
# calculate_investment function computes the investment value 
# over time by assuming an initial investment of $10,000.

# 2.2.2 Graph Plotting
# The display_chart function plots the stock data using mplfinance. 
# It resamples the data into weekly intervals and displays the chart 
# showing the investment value over time.

# 2.2.3 User Input and Results Display
# The get_ticker_symbol function opens a dialog where users input 
# a stock ticker symbol. The display_results function shows the 
# investment details (ticker, buy price, final value) in the result 
# box.

# 2.2.4 Text Scaling
# The zoom_text function allows users to dynamically adjust the 
# text size in the results display using a slider.

# 2.3 GUI Components
# - Chart Frame: Displays the stock price chart.
# - ScrolledText Widget: Shows investment calculation results.
# - Zoom Slider: Allows dynamic text size adjustment.
# - Buttons: To backtest a stock or exit the application.

# -------------------------------------------------------------

# 3. How to Use the Application

# 1. Running the Application:
# - Run the Python script in an environment with the required libraries.

# 2. Entering a Ticker Symbol:
# - Click the "Backtest Stock" button and input a valid stock ticker 
#   symbol (e.g., "AAPL" for Apple, "GOOGL" for Alphabet).

# 3. Viewing Results:
# - The tool fetches historical data and calculates:
#   - Initial investment: $10,000
#   - Buy price (first closing price)
#   - Final investment value (based on final closing price)
#   - A line chart is displayed showing weekly stock performance.

# 4. Adjusting Text Size:
# - Use the "Text Zoom" slider to adjust the font size of the 
#   displayed results.

# 5. Exiting the Application:
# - Click the "Exit" button to close the program.

# -------------------------------------------------------------

# 4. Future Feature Expansion Plans

# 4.1 Additional Metrics and Indicators
# - Add Moving Averages (MA) and other technical indicators like 
#   RSI, Bollinger Bands, and MACD to provide more insights.

# 4.2 Custom Date Range Selection
# - Allow users to input custom start and end dates for backtesting 
#   flexibility.

# 4.3 Compare Multiple Stocks
# - Provide support for comparing multiple stocks on the same chart 
#   and analyzing portfolio performance.

# 4.4 Export Results
# - Add options to export the backtested data to CSV files or 
#   generate PDFs of the charts and results.

# 4.5 Real-Time Data Integration
# - Implement real-time stock price fetching and update the chart 
#   dynamically with live data.

# 4.6 Graphical Enhancements
# - Add more interactive charts (zoom, pan, hover for details) and 
#   customizable themes and colors.

# 4.7 Risk Analysis Tools
# - Implement risk analysis features like Value at Risk (VaR) and 
#   the Sharpe Ratio to evaluate risk-adjusted returns.

# -------------------------------------------------------------

# 5. Conclusion
# The Investment Backtest Tool provides a simple and intuitive 
# interface for stock performance analysis over time. With planned 
# future updates, it can become a comprehensive tool for financial 
# analysis, offering more advanced features such as technical 
# indicators, real-time data, and risk analysis.
#-------------------------------------------------------------
import pandas as pd
import yfinance as yf
import mplfinance as mpf
import tkinter as tk
from tkinter import scrolledtext, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Constants for default investment details
INITIAL_INVESTMENT = 10000
START_DATE = "2009-01-01"
END_DATE = "2024-01-01"

# Fetch historical data function
def fetch_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

# Calculate investment value over time
def calculate_investment(data, initial_investment):
    buy_price = data['Close'].iloc[0]
    stock_value = initial_investment / buy_price
    data['Investment Value'] = stock_value * data['Close']
    return data, buy_price, data['Investment Value'].iloc[-1]

# Resample data to weekly
def resample_data(data):
    return data.resample('W').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    })

# Function to get user input for the ticker symbol
def get_ticker_symbol():
    return simpledialog.askstring("Input", "Enter the ticker symbol:", parent=root)

# Function to display the results in the GUI
def display_results(ticker, initial_investment, buy_price, final_value):
    results = (
        f"Ticker Symbol: {ticker}\n"
        f"Initial Investment: ${initial_investment:,.2f}\n"
        f"Buy Price: ${buy_price:,.2f}\n"
        f"Final Investment Value: ${final_value:,.2f}\n"
    )
    text_area.delete(1.0, tk.END)  # Clear previous text
    text_area.insert(tk.END, results)

# Function to display the chart in the GUI
def display_chart(data):
    data_resampled = resample_data(data)

    custom_style = mpf.make_mpf_style(
        base_mpf_style='charles',
        marketcolors=mpf.make_marketcolors(up='green', down='red'),
        facecolor='#2E2E2E', gridcolor='#4F4F4F'
    )

    fig, ax = mpf.plot(
        data_resampled, type='line', style=custom_style, title='Investment Value Over Time',
        ylabel='Value ($)', returnfig=True
    )

    ax[0].xaxis.set_major_locator(plt.MaxNLocator(15))
    ax[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

    # Clear any previous canvas widgets
    for widget in chart_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    canvas.mpl_connect('scroll_event', on_chart_zoom)

# Function to zoom the text area
def zoom_text(event):
    scale = text_zoom.get()
    text_area.config(font=("TkDefaultFont", scale))

# Function to zoom the chart
def on_chart_zoom(event):
    ax = event.inaxes
    if not ax:
        return

    scale_factor = 1.1 if event.button == 'up' else 0.9 if event.button == 'down' else 1
    ax.set_xlim([event.xdata - (event.xdata - ax.get_xlim()[0]) * scale_factor,
                 event.xdata + (ax.get_xlim()[1] - event.xdata) * scale_factor])
    ax.set_ylim([event.ydata - (event.ydata - ax.get_ylim()[0]) * scale_factor,
                 event.ydata + (ax.get_ylim()[1] - event.ydata) * scale_factor])
    event.canvas.draw()

# Function to make the text area draggable
def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)

def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

# Function to handle exiting the program
def on_exit():
    root.quit()
    root.destroy()

# Function to backtest a stock based on user input
def backtest_stock():
    ticker = get_ticker_symbol()
    if not ticker:
        return  # User pressed cancel or entered an empty string

    data = fetch_data(ticker, START_DATE, END_DATE)
    if data.empty:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, f"No data found for {ticker}.")
        return

    data, buy_price, final_value = calculate_investment(data, INITIAL_INVESTMENT)

    # Display results and chart for the given ticker
    display_results(ticker, INITIAL_INVESTMENT, buy_price, final_value)
    display_chart(data)

# Create the main window
root = tk.Tk()
root.title("Investment Backtest Tool")

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_exit)

# Create a frame for the chart
chart_frame = tk.Frame(root)
chart_frame.pack(fill=tk.BOTH, expand=True)

# Create a scrolled text widget for results, placed below the chart
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10)
text_area.pack(fill=tk.X, padx=10, pady=10)

# Add zoom slider for text scaling
text_zoom = tk.Scale(root, from_=10, to=40, orient=tk.HORIZONTAL, label="Text Zoom", command=zoom_text)
text_zoom.set(12)
text_zoom.pack(fill=tk.X, padx=10, pady=5)

# Add buttons for backtesting and exiting
backtest_button = tk.Button(root, text="Backtest Stock", command=backtest_stock)
backtest_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=on_exit)
exit_button.pack(pady=10)

# Run the tkinter main loop
root.mainloop()
