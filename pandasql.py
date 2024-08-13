import pandasql as ps
print(ps)
import pandas as pd
from pandasql import sqldf
import time

if __name__ == '__main__':
    start = time.time()
    tax10w = pd.read_csv('tax_10w.csv', dtype={'salary':float, 'rate':float, 'singleexemp':float, 'marriedexemp':float, 'childexemp': float})
    print(f'read csv {time.time() - start}s')

    resule = sqldf('SELECT COUNT(*) FROM tax10w;', tax10w)
    print(resule)




