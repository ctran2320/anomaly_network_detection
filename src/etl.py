# code for preprocessing and cleaning our data and features
import pandas as pd

## aggregate_data returns a pandas dataframe with mean of total packets sent as the feature and a window size of n
## data is a list of csv files from DANE runs
## n is a paramter to change the window size of network traffic. i.e. n=20 would transform the dataset into 20 second windows
def aggregate_data(data, n):
    df = pd.DataFrame(pd.read_csv(data[0])[20:].reset_index().drop('index',axis=1))  # reads in first file and removes first 20 seconds of data
    df['total_pkts'] = df['1->2Pkts'] + df['2->1Pkts']     # calculates total packet sent
    df = df[df['total_pkts'] >1].reset_index().drop('index',axis=1) # removes insignificant amount of packet sent 
    for file in data[1:]:                                   # loops through rest of the csv files and repeats process as above
        dff = pd.DataFrame(pd.read_csv(file)[20:]).reset_index().drop('index',axis=1)
        dff['total_pkts'] = dff['1->2Pkts'] +df['2->1Pkts']
        dff = dff[dff.total_pkts > 1].reset_index().drop('index',axis=1)
        df=  pd.concat([df,dff],ignore_index=True)           # concatenates data
    df = df[:len(df) - (len(df) %n)]                      # Ensures that final dataset size is divisible by n. i.e. if n = 20 and length of df is 523, then removes last 3 datapoints so df is length 520
    ## Aggregates data into size n windows with mean of total packets as feature
    df_agg = pd.DataFrame([df[:n]['total_pkts'].mean()],index=['total_pkts']).T
    for i in range(n,df.shape[0],n):
        df_agg = pd.concat([df_agg,pd.DataFrame([df[i:i+n]['total_pkts'].mean()],index=['total_pkts']).T],ignore_index=True)
    return df_agg
