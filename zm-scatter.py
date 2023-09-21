import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zscore
from datetime import datetime


def plot_time_scores(csv_path: str) -> None:
    """
    Reads in a csv file and plots time scores over date-time.
    
    Parameters:
    - csv_path (str): Path to the csv file.
    
    Returns:
    - None. Displays the plot.
    """
    # To Do: colour code by 'sessions (points reasonably clustered) and this could be alternating
    
    # Read data from the csv file
    df = pd.read_csv(csv_path)

    # Convert timestamp to datetime format
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

    # Apply a sqrt transform to the data to stablise the variance and centre the mean
    #df['transformed_time'] = df['timetaken'].apply(lambda x: np.sqrt(x))
    df['log_time'] = df['timetaken'].apply(lambda x: np.log(x+0.001))
    #df['zscore_time'] = zscore(df['transformed_time'])

    # Compute 50 wide rolling average
    df['rolling_avg'] = df['log_time'].rolling(window=200, min_periods=50).mean()
    
    # Map colors based on whether the answer was correct or wrong
    colours = df['got_wrong'].map({True: 'red', False: 'green'}) 
    
    # Plot using Seaborn
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x=df.index, 
        y=df['log_time'], 
        hue=df['got_wrong'],
        palette={True: 'red', False: 'green'},
        style=df['got_wrong'],
        markers={True: 'X', False: 'o'},
        sizes=10,  # Adjusted sizes for smaller dots
        alpha=0.6
    )    

    # Adding the 50-point rolling average line to the plot
    sns.lineplot(x=df.index, y=df['rolling_avg'], color='blue', label='50-pt Rolling Avg')  

    # Improve x-axis labeling
    plt.xticks(rotation=45)
   #plt.gca().set_xticks(plt.gca().get_xticks()[::int(len(df['datetime'])/10)]) 

    plt.xlabel('Sequence of Attempts')
    plt.ylabel('Time Taken (Log Transformed)')
    plt.title('Time Scores Distribution Over Time Based on Correctness')
    plt.grid(True, which="both", ls="--", c='0.7')  # Adding a grid for better readability
    plt.legend(title='First try', loc='upper right', labels=['Yes', 'No'])
    plt.axhline(y=1, color='yellow', linestyle='--')
    plt.text(1, 2, 'e seconds per question')

    # Adjust layout
    plt.tight_layout()

    # SAVE

    # Get current date
    today = datetime.today()
    formatted_date = today.strftime("%d-%m-%y")
    plt.savefig(f"scatter-upto-{df.index[-1]}-{formatted_date}", dpi=300)
    print('Plot created and saved')

    # SHOW
    # plt.show()

if __name__ == "__main__":
    csv_path = str(input("Enter the name of the csv file: ")) + '.csv'
    plot_time_scores(csv_path)