import pandas as pd
import os
from pathlib import Path

# here is where you put or call all your logic for data mining 
# and so forth. the best would be to define a method that 
# gets data and put it into a file and then  call the below method 
# to get the data.

# or you can just return the data as a pandas df to the invoker
# instead of saving to a file.


def getData():
    try:
        df =  pd.read_csv(str(Path('data\\new_data.csv')))
        return df

    except:
        print("Data not found..")
        return ''