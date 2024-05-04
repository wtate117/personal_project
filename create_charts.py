import pandas as pd

from common_imports import tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from data_retrieval import retrieve_stock_data_dynamic, retrieve_stock_data_static
from date_utils import get_start_date
from common_imports import AutoDateLocator, AutoDateFormatter, datetime


def create_line_chart(data_set, ticker, start_date, end_date):
    # end_date, start_date = get_start_date(time_unit, time_frame)
    # data_set, ticker = retrieve_stock_data_static(ticker, start_date, end_date)

    # Create a Matplotlib figure and a subplot
    fig = Figure(figsize=(10, 6), dpi=100)
    plot = fig.add_subplot(1, 1, 1)

    # Remove the hour component
    # Convert 'timestamp' column to datetime format
    data_set['time'] = pd.to_datetime(data_set['time'])

    data_set['time'] = data_set['time'].apply(lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0))

    # Plot data on the subplot
    # name = data_set.info.get('longName')
    fig.suptitle(f'Adj Closing Price for {ticker} from {start_date} to {end_date}')
    plot.plot(data_set['time'], data_set['close'], color='green', linewidth=0.5)

    # Set the x-ticks dynamically
    locator = AutoDateLocator()
    formatter = AutoDateFormatter(locator)
    plot.xaxis.set_major_locator(locator)
    plot.xaxis.set_major_formatter(formatter)
    """
    # Define a custom function to format the dates
    def custom_date_formatter(x, pos=None):
        if isinstance(x, float):
            date = datetime.fromtimestamp(x)
        else:
            date = datetime.fromisoformat(x.get_text())
        return date.strftime('%Y-%m-%d')  # Format the date as desired
    """

    # Optional: Enhance readability
    fig.autofmt_xdate()  # Automatically adjusts the x-tick labels to fit and prevent overlap

    return fig
