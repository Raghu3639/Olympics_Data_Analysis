import pandas as pd

def preprocess(data, region):

    # Changing the whole olympic data into summer olympic data
    data = data[data['Season'] == 'Summer']
    # Merging the region column into the data
    data = data.merge(region, on='NOC', how='left')
    # Checking duplicate values and removing
    data.drop_duplicates(inplace=True)
    # Counting the medals and converting them into columns and concatenate into actual data
    data = pd.concat([data, pd.get_dummies(data['Medal'])], axis=1)
    return data
