'''
The module writes code to give descriptive statistics such as mean, median, mode, range etc.

Modularize the code. Build and publish a package using the procedures described in Chapter 2 of your textbook to TestPyPI.

Install and use your package in your own code as you would any official Python library. 

The goal of this assignment is for you to demonstrate Modularization. 

Remember to describe the dataset and all the steps you did in the readme.md file.
'''
# Function to give descriptive statistics (mean, median, mode, range) of a DataFrame
def descriptive_statistics(df):
    '''
    Docstring for descriptive_statistics
    
    The input is a pandas DF and the output should be a description stats of all columns.
    '''
    description = df.describe()
    return description
# Function to calculate mean
def mean(df, column_name):
    '''
    Docstring for mean
    
    :param df: DataFrame
    :param column_name: str
    :return: float
    '''
    return df[column_name].mean()

# Function to calculate median
def median(df, column_name):
    '''
    Docstring for median
    
    :param df: DataFrame
    :param column_name: str
    :return: float
    '''
    return df[column_name].median()

# Function to calculate mode
def mode(df, column_name):
    '''
    Docstring for mode
    
    :param df: DataFrame
    :param column_name: str
    :return: Series
    '''
    return df[column_name].mode()

# Function to calculate range
def data_range(df, column_name):
    '''
    Docstring for data_range
    
    :param df: DataFrame
    :param column_name: str
    :return: float
    '''
    return df[column_name].max() - df[column_name].min()

# Function to calculate variance
def variance(df, column_name):
    '''
    Docstring for variance
    
    :param df: DataFrame
    :param column_name: str
    :return: float
    '''
    return df[column_name].var()