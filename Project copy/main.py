import module_02 as m2
import module_01 as m1
import module_03 as m3
import module_04 as m4
import module_06_07 as m6
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import asyncio

#Module 1 & 2 work
#create the format of main.py
def main():
    #print("Hello User!")
    file = 'Australian_weather_data/Weather Training Data.csv'
    #m1.print_hi('VC_Code_User')
    data = m1.read_csv_file(file)
    #print(data.head())
    stats = m2.descriptive_statistics(data)
    filtered_data = data[['Location', 'MinTemp', 'MaxTemp', 'Rainfall','Humidity9am', 'Humidity3pm']]
    """
    #print(stats)
    print (data.columns)


    # Module_03 work
 
    max_temp_row = filtered_data.loc[filtered_data['MaxTemp'].idxmax()]
    min_temp_row = filtered_data.loc[filtered_data['MinTemp'].idxmin()]
    print("\n\nRecords with Extreme Temperatures:")
    max_temp_record = m3.create_weather_record(
        location=max_temp_row['Location'],
        min_temp=max_temp_row['MinTemp'],
        max_temp=max_temp_row['MaxTemp'],
        rainfall=max_temp_row['Rainfall'])

    min_temp_record = m3.create_weather_record(
        location=min_temp_row['Location'],
        min_temp=min_temp_row['MinTemp'],
        max_temp=min_temp_row['MaxTemp'],
        rainfall=min_temp_row['Rainfall'])
    
    print("Max Temperature Record:")
    print(max_temp_record)
    print("Min Temperature Record:")
    print(min_temp_record)
    print("\n\nCreating City Instances:")
    print("\nMaking City Instance for Max Temperature Record:")
    #Humidity is the average humidity of te city at 9am and 3pm
    city_max_temperature = m3.create_city(name= max_temp_record.location, humidity= (filtered_data.loc[filtered_data['Location'] == max_temp_record.location, 'Humidity3pm'].values[0]+ filtered_data.loc[filtered_data['Location'] == max_temp_record.location, 'Humidity9am'].values[0])/2)
    city_min_temperature = m3.create_city(name= min_temp_record.location, humidity= (filtered_data.loc[filtered_data['Location'] == min_temp_record.location, 'Humidity3pm'].values[0]+ filtered_data.loc[filtered_data['Location'] == min_temp_record.location, 'Humidity9am'].values[0])/2)
    print(city_max_temperature)
    print("\n\nMaking another City Instance for Min Temperature Record:")
    print(city_min_temperature)
    print('\n\n')
"""
    # Module_04 work
    print("Iterating through filtered DataFrame and printing rows:")
    m4.iterate_and_print_df(filtered_data.head(5))  # Print first 5 rows for brevity

    """
    print("\nUsing AU_dataFrame_Iter to iterate through DataFrame:")
    for row in df_iterator:
        print(f"Row: {row['Location']}, {row['MinTemp']}, {row['MaxTemp']}, {row['Rainfall']}")
    
    print("\nTesting StopIteration exception:")
    print(next(df_iterator))  # This will raise StopIteration
    print(next(df_iterator))  # This will raise StopIteration
    print(next(df_iterator))  # This will raise StopIteration
"""
    window_trends_iterator = m4.Window_trends(filtered_data.head(10), window_size=3)
    print("\nUsing Window_trends to iterate through DataFrame in windows:")
    for i, window in enumerate(window_trends_iterator):
        print(f"Window {i+1}:")
        print(window[['Location', 'MinTemp', 'MaxTemp', 'Rainfall']])
    # Using Generator
    
    #for row in filtered_data.iterrows():
    #    print(f"Row: {row[1]['Location']}, {row[1]['MinTemp']}, {row[1]['MaxTemp']}, {row[1]['Rainfall']}")

    df_gen_chunks = m4.weather_chunks(filtered_data.head(10), chunk_size=3)
    print("\nUsing weather_chunks to iterate through DataFrame in chunks:")
    for i, chunk in enumerate(df_gen_chunks):
        print(f"Chunk {i+1}:")
        print(chunk[['Location', 'MinTemp', 'MaxTemp', 'Rainfall']])



    #Logs
    m4.load_logging_config()

    print(filtered_data['MaxTemp'].head())
    print(filtered_data['MinTemp'].head())
    print(filtered_data.head())

    plt.figure(figsize=(10, 5))
    # Plot of bars with the different locations on the x-axis and the average max temperature on the y-axis
    avg_max_temp = filtered_data.groupby('Location')['MaxTemp'].mean()
    avg_max_temp.plot(kind='bar', color='skyblue')
    plt.title('Average Max Temperature by Location')
    plt.xlabel('Location')
    plt.ylabel('Average Max Temperature')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# New Main function
async def main2():
    #Reading file...
    file = 'Australian_weather_data/Weather Training Data.csv'
    data = m1.read_csv_file(file)

    #Descriptive stats
    stats = m2.descriptive_statistics(data)

    #Filtered data, cleaned and derived
    filtered_data = data[['Location', 'MinTemp', 'MaxTemp', 'Rainfall','Humidity9am', 'Humidity3pm']]
    clean = m6.prepare_weather_df(filtered_data)
    derived = m6.add_derived(clean)

    batch = asyncio.gather(m6.filter_hot_days(derived, threshold=35), m6.total_rainfall(derived), m6.top_locations_by_avg_max_temp(derived, top_n=10), m6.make_plots(derived, out_dir="static/img/"))
    hot_df, totalRainfall, top_hot, plot_files = await batch

    #Data anlysis for filtered data 1 async
    print(hot_df)
    print("Hot days count:", len(hot_df))

    #Data anlysis for filtered data 2 async
    print("Total rainfall:", totalRainfall)

    #Data analysis for filtered data 3 async
    print(top_hot)

    #Graph generation async
    print("\n\nSaved plots:")
    for f in plot_files:
        print(" -", f)

if __name__ == "__main__":
  asyncio.run(main2())
