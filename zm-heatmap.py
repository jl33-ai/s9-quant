import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

operation_dict = {
        '+' : 'Addition', 
        '-' : 'Subtraction', 
        '*' : 'Multipliation', 
        '/' : 'Division'
    }

def aggregate_zmatx(): 
    """
    This function should aggregate all the scores across all available .csv data 
    Or just for a specific .csv 
    """
    return 

def generate_heatmap(operation, df):
    """
    Generate a heatmap based on the operation provided.
    
    Parameters:
        - operation (str): The operation to generate the heatmap for. One of ['+', '-', '*', '/'].
        - df (pandas.DataFrame): The data containing the timestamp, num1, operator, num2, and timetaken columns.

    In future, may be used on data aggregrated from a population of zetamatrices... i.e not just one user. 
    Will do this with a simple average over each cell.
    """

    # Filter the DataFrame based on operation
    operation_df = df[df['operator'] == operation]
    operation_df['log_time'] = df['timetaken'].apply(lambda x: np.log(x+0.001))
    
    # If there's no data for this operation, just return
    if operation_df.empty:
        print(f"No data available for operation: {operation}")
        return
    
    # Create an empty matrix filled with ( , ), depending on dimensions of operation
    if operation in ['+', '-']:
        matrix = np.full((99, 99), np.nan)
    else: 
        matrix = np.full((11, 99), np.nan)
    
    # Populate the matrix using the data from the DataFrame
    # MUST AMEND THIS SO THAT IT ONLY UPDATES WITH FASTER TIMES
    # Also store a counter for how many unique combos have been tried 
    for index, row in operation_df.iterrows():
        matrix[int(row['num1'])-2][int(row['num2'])-2] = row['log_time']
    
    # Generate the heatmap
    plt.rcParams["font.family"] = "Courier"  # change 'Arial' to any font you prefer
    plt.rcParams["font.size"] = 8  # Adjust the size accordingly
    plt.figure(figsize=((12, 3)))
    sns.heatmap(matrix, cmap='viridis_r')
    plt.title(f"Heatmap for {operation_dict[operation]}")
    plt.xlabel('num2')
    plt.xticks(rotation=45)
    plt.ylabel('num1')

    yticks = plt.gca().get_yticks()

    # Adjust the labels by adding 2
    new_labels = yticks + 2

    # Set the new y-axis tick labels
    plt.gca().set_yticklabels(new_labels)

    plt.savefig(f"zetamatrix-{df.index[-1]}-{operation}", dpi=300)
    plt.clf()
    # plt.show()
    
def generate_heatmaps_from_csv(filename='new_data.csv'):
    """
    Read data from the CSV file and generate heatmaps for each operation.
    
    Parameters:
        - filename (str): The path to the CSV file to read data from.
    """
    df = pd.read_csv(filename)

    # For each operation, generate a heatmap
    #for operation in ['+', '-', '*']:
     #   generate_heatmap(operation, df)
    generate_heatmap('*', df)

# If this module is run as a script, generate the heatmaps
if __name__ == "__main__":
    generate_heatmaps_from_csv()
