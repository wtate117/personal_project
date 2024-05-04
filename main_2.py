from common_imports import tk, pd, np
from crypto_data_pull import full_data_pull_process
from tkinter import ttk
from date_utils import get_start_date
from neural_network_function import load_and_preprocess_data, run_all_functions
from create_charts import create_line_chart

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Assuming necessary imports and functions are available
from date_utils import get_start_date

# from crypto_data_pull import full_data_pull_process  # This needs to be defined
# from create_charts import create_line_chart  # This needs to be defined
global start_date, end_date
# make a global dictionary of crypto currencies
crypto_dict = {
    "Bitcoin": "BTC",
    "Ethereum": "ETH",
    "Ripple": "XRP",
    "Cardano": "ADA",
    'Solana': "SOL",
    "Dogecoin": "DOGE"

    # Add more mappings as needed
}
crypto_names = list(crypto_dict.keys())


def parse_date_values(period_combobox):
    selected_timehorizon = period_combobox.get()
    if selected_timehorizon == 'YTD':
        time_unit = 'YTD'
        time_frame = 1
    else:
        string_cut_position = len(selected_timehorizon) - 1  # position to pull the time frame
        time_unit = selected_timehorizon[-1]
        time_frame = int(selected_timehorizon[0:string_cut_position])
    return time_unit, time_frame


def get_dates(period_combobox):
    global start_date, end_date
    time_unit, time_frame = parse_date_values(period_combobox)
    end_date, start_date = get_start_date(time_unit, time_frame)
    return start_date, end_date


def pull_data(crypto_currency):
    # pull data
    dataset = full_data_pull_process(start_date, end_date, crypto_currency)
    dataset = dataset.drop(dataset.columns[0], axis=1)
    print(dataset.head())
    # print the first 20 rows and the last 20 rows to the console

    return dataset


def graph_closing_prices(df, currency, plot_frame):
    # global start_date, end_date
    # graph the closing prices
    fig = create_line_chart(df, currency, start_date, end_date)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=0, columnspan=3, sticky="nsew")
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def display_data(df, text_widget):
    text_widget.delete('1.0', tk.END)  # Clear existing text
    text = "First 20 Rows:\n" + df.head(20).to_string() + "\n\nLast 20 Rows:\n" + df.tail(20).to_string()
    text_widget.insert(tk.END, text)

def get_crypto_symbol(currency_name):
    """
    Get the symbol for a cryptocurrency based on its name.

    Args:
    - currency_name (str): The name of the cryptocurrency.
    - crypto_dict (dict): A dictionary mapping cryptocurrency names to symbols.

    Returns:
    - str: The symbol of the cryptocurrency, or None if not found.
    """
    return crypto_dict.get(currency_name)

def predict_next_closing_price(df):
    predictions = run_all_functions(df)
    return predictions


def submit_action(crypto_combobox, period_combobox, data_text, plot_frame):
    currency = get_crypto_symbol(crypto_combobox.get().upper())
    global start_date, end_date
    start_date, end_date = get_dates(period_combobox)
    # Pull data
    df = pull_data(currency)
    display_data(df, data_text)
    # Graph the closing prices
    graph_closing_prices(df, currency, plot_frame)
    # prediction = predict_next_closing_price(df)
    # prediction_label.config(text=f"Next predicted closing price for {currency}: {prediction:.2f}")


def main():
    root = tk.Tk()
    root.title("Crypto Time Period Evaluation")

    tab_control = ttk.Notebook(root)

    # Data Tab
    data_tab = ttk.Frame(tab_control)
    tab_control.add(data_tab, text='Data View')
    data_text = tk.Text(data_tab, height=10, width=50)
    data_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Plot Tab
    plot_tab = ttk.Frame(tab_control)
    tab_control.add(plot_tab, text='Closing Price Plot')

    tab_control.pack(expand=1, fill="both")

    """prediction_tab = ttk.Frame(tab_control)
    tab_control.add(prediction_tab, text='Price Prediction')
    prediction_label = ttk.Label(prediction_tab, text="Prediction will be shown here.")
    prediction_label.pack(pady=20)
    """
    # Frame for Combobox and Entry
    frame = ttk.Frame(root, padding=(20, 10))
    frame.pack(side=tk.TOP, fill=tk.X)

    # Combobox for selecting cryptocurrency
    ttk.Label(frame, text="Select a Cryptocurrency:").pack(side=tk.LEFT)

    crypto_combobox = ttk.Combobox(frame, values=crypto_names)
    crypto_combobox.pack(side=tk.LEFT)

    # Combobox for selecting period
    ttk.Label(frame, text="Select Evaluation Period:").pack(side=tk.LEFT)
    period_combobox = ttk.Combobox(frame, values=["1M", "3M", "1Y", "5Y", "YTD"])
    period_combobox.pack(side=tk.LEFT)

    # Submit button
    submit_button = ttk.Button(frame, text="Grab Data",
                               command=lambda: submit_action(crypto_combobox, period_combobox, data_text, plot_tab,))
    submit_button.pack(side=tk.LEFT)

    root.mainloop()


if __name__ == "__main__":
    main()
