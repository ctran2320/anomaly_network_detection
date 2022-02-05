# code for preprocessing and cleaning our data and features
import pandas as pd

def aggregate_data(data, n):
    df = pd.DataFrame(pd.read_csv(data[0])[20:].reset_index().drop('index',axis=1))
    df['total_pkts'] = df['1->2Pkts'] + df['2->1Pkts']
    df = df[df['total_pkts'] >1].reset_index().drop('index',axis=1)
    for file in data[1:]:
        dff = pd.DataFrame(pd.read_csv(file)[20:]).reset_index().drop('index',axis=1)
        dff['total_pkts'] = dff['1->2Pkts'] +df['2->1Pkts']
        dff = dff[dff.total_pkts > 1].reset_index().drop('index',axis=1)
        df=  pd.concat([df,dff],ignore_index=True)
    df = df[:len(df) - (len(df) %n)]
    df_agg = pd.DataFrame([df[:n]['total_pkts'].mean()],index=['total_pkts']).T
    for i in range(n,df.shape[0],n):
        df_agg = pd.concat([df_agg,pd.DataFrame([df[i:i+n]['total_pkts'].mean()],index=['total_pkts']).T],ignore_index=True)
    return df_agg
