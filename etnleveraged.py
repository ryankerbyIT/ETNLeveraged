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