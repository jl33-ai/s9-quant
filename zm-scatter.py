import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_time_scores(csv_path: str) -> None:
    """
    Reads in a csv file and plots time scores over date-time.
    
    Parameters:
    - csv_path (str): Path to the csv file.
    
    Returns:
    - None. Displays the plot.
    """
    
    # Read data from the csv file
    df = pd.read_csv(csv_path)

    # Convert timestamp to datetime format
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # Map colors based on whether the answer was correct or wrong
    colours = df['got_wrong'].map({True: 'red', False: 'green'})
    
    # Plot using Seaborn
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df.index, y=df['timetaken'], color=colours)

    plt.xticks(rotation=45)
    plt.xlabel('Date-Time')
    plt.ylabel('Time Taken')
    plt.title('Dot Plot of Time Scores over Date-Time')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    csv_path = '/Users/justinlee/Documents/projport/s9-quant/data.csv'
    plot_time_scores(csv_path)
