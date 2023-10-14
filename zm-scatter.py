import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zscore
from datetime import datetime
import matplotlib as mpl


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
    # Apply a sqrt transform to the data to stablise the variance and centre the mean
    log_times = df['timetaken'].apply(lambda x: np.log(x + 0.001))
    print(log_times.head())
    #df['zscore_time'] = zscore(df['transformed_time'])

    # Compute 50 wide rolling average
    #df['rolling_avg'] = df['log_time'].rolling(window=200, min_periods=50).mean()
    
    # Map colors based on whether the answer was correct or wrong
    colours = df['got_wrong'].map({True: 'red', False: 'black'})
    markers={True: 'X', False: 'o'}

    # Set the font to be professional (Times New Roman)
    sns.set(font="Times New Roman")

    # Plot using Seaborn
    plt.figure(figsize=(10, 6))
    '''
    sns.scatterplot(
        x=df.index,
        y=df['log_time'],
        hue=df['got_wrong'],
        facecolors='none',
        edgecolor=colours,  # Edge colors as before
        linewidth=0.5,  # Line width of marker edges
        style=df['got_wrong'],
        markers={True: 'X', False: 'o'},
        s=15,  # Adjusted sizes for smaller dots
        alpha=0.8
    )
    '''
    plt.scatter(log_times.index, log_times, facecolors='none', edgecolors=colours, linewidth=0.5, s=10, alpha=0.95)

    # Adding the 50-point rolling average line to the plot
    #plt.plot(x=df.index, y=df['rolling_avg'], color='blue', label='50-pt Rolling Avg')

    # Improve x-axis labeling
    plt.xticks(rotation=45) #Bruh
    plt.xlabel('Sequence of Attempts')
    plt.ylabel('Time Taken (Log Transformed)')
    plt.title('Time Scores Distribution Over Time Based on Correctness')
    #plt.grid(True, which="both", ls="--", c='0.7')
    #plt.legend(title='First try', loc='upper right', labels=['Yes', 'No'])
    #plt.axhline(y=1, color='orange', linestyle='--')
    plt.text(1, 1.5, 'e=2.17 seconds per question', fontname="Times New Roman")

    # Adjust layout
    ##plt.tight_layout()

    # Save
    today = datetime.today()
    formatted_date = today.strftime("%d-%m-%y")
    #plt.savefig(f"katrina-scatter-upto-{df.index[-1]}-{formatted_date}", dpi=300)
    plt.savefig('new-plot', dpi=300)
    print('Plot created and saved')

    
if __name__ == "__main__":
    # csv_path = str(input("Enter the name of the csv file: ")) + '.csv'
    plot_time_scores('/Users/justinlee/Documents/projport/s9-quant/new_data.csv')
    try: 
        pass
    except:
        print("Could not find that file.")

        # chips