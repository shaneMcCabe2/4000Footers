import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect('footers.db') 
c = conn.cursor()
                 
data = c.execute('''
          SELECT
          *
          FROM footers
          ''')

columns = []

for column in data.description:
    columns = np.append(columns, column[0])

df = pd.DataFrame(c.fetchall(), columns = columns)
pd.set_option('display.max_columns', None)
print (df)