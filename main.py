from common_imports import tk, ttk, FigureCanvasTkAgg
from crypto_data_pull import full_data_pull_process
from date_utils import get_start_date
from neural_network_function import load_and_preprocess_data
from create_charts import create_line_chart


def get_dates():
    # create start and end dates
    time_unit, time_frame = parse_date_values()
    end_date, start_date = get_start_date(time_unit, time_frame)

    return start_date, end_date


def pull_data(crypto_currency, start_date, end_date):
    # pull data
    dataset = full_data_pull_process(start_date, end_date, crypto_currency)

    columns_to_drop = ['time', 'conversionType', 'conversionSymbol']
    df = dataset.drop(columns_to_drop, axis=1)

    # print the first 20 rows and the last 20 rows to the console

    return df


def graph_closing_prices(df, start_date, end_date, currency):
    # graph the closing prices
    fig = create_line_chart(df, currency, start_date, end_date)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=0, columnspan=3, sticky="nsew")
    canvas.draw()
    # run the neural network


# Splits the user selected timeframe from the drop down menu into values to be used in the date functions
def parse_date_values():
    selected_timehorizon = period_combobox.get()
    if selected_timehorizon == 'YTD':
        time_unit = 'YTD'
        time_frame = 1
    else:
        # Define the start and end dates
        string_cut_position = len(selected_timehorizon) - 1  # position to pull the time frame
        time_unit = selected_timehorizon[-1]
        time_frame = int(selected_timehorizon[0:string_cut_position])
    return time_unit, time_frame


def main():
    # Root window
    root = tk.Tk()
    root.title("Crypto Time Period Evaluation")

    # Frame for Combobox and Entry
    frame = ttk.Frame(root, padding=(20, 10))
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

    # Label for cryptocurrency selection
    ttk.Label(frame, text="Select a Cryptocurrency:").grid(row=0, column=0)

    # Combobox for selecting cryptocurrency
    crypto_combobox = ttk.Combobox(frame, values=["Bitcoin", "Ethereum", "Ripple", "Litecoin"])
    crypto_combobox.grid(row=0, column=1)
    currency = crypto_combobox.get().upper()

    # Label for period selection
    ttk.Label(frame, text="Select Evaluation Period:").grid(row=1, column=0)

    # Combobox for selecting period
    period_combobox = ttk.Combobox(frame, values=["1M", "3M", "1Y", "5Y", "YTD"])
    period_combobox.grid(row=1, column=1)

    # create variables for the start and end dates
    start_date, end_date = get_dates()

    # Submit button
    submit_button = ttk.Button(frame, text="Grab Data", command=pull_data(start_date, end_date))
    submit_button.grid(row=2, column=0, columnspan=2)

    crypto_data = pull_data(currency, start_date, end_date)

    # graph a line chart of the closing prices
    graph_closing_prices(crypto_data, start_date, end_date, currency)

    # Label for displaying results
    result_label = ttk.Label(root, text="Result will be shown here.", padding=(20, 10))
    result_label.grid(row=2, column=0, sticky=(tk.W, tk.E))

    # Start the GUI
    root.mainloop()
    # Comment out the call to `root.mainloop()` when developing in the PCI.


if __name__ == "__main__":
    main()
