def print_hi(name):
    '''
    Docstring for print_hi
    
    :param name: None
    '''
    print(f'Hi, {name}:')

# Function to open the csv file and read its contents using pandas
import pandas as pd
import sys

def read_csv_file(file_path):
    '''
    Docstring for read_csv_file
    
    :param file_path: str
    :return: DataFrame
    '''
    df = pd.read_csv(file_path)
    return df


# This function will be moved to the main.py file on future modules.
if __name__ == '__main__':
    file = 'Australian_weather_data/Weather Training Data.csv'
    print_hi('VC_Code_User')
    data = read_csv_file(file)
    print(data.head())
    print(sys.modules.keys())
