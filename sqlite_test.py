
import time
import sqlite3
import pandas as pd

db = sqlite3.connect(':memory:')

start = time.time()
df = pd.read_csv('tax100w.csv', dtype={'salary':float, 'rate':float, 'singleexemp':float, 'marriedexemp':float, 'childexemp': float})
df.to_sql('tax100w', db, if_exists='append', index=False)
print(f'read csv {time.time() - start}s')

# 表长度计算
start = time.time()
print('table length', db.execute('SELECT COUNT(1) FROM tax100w').fetchone())
print(f'SELECT COUNT(1) {time.time() - start}s')

# 计算每个州的平均工资
# SELECT state, AVG(salary) FROM tax100w GROUP BY state
start = time.time()
for row in db.execute('SELECT state, AVG(salary) average FROM tax100w GROUP BY state ORDER BY average DESC LIMIT 2').fetchall():
    print(row)
print(f'计算每个州的平均工资 {time.time() - start}s')

# 计算每个州大于平均工资的人比例
start = time.time()
for row in db.execute('''SELECT t3.state, SUM(t3.gt) / COUNT(t3.gt) AS rate FROM 
                        (SELECT t0.state, (CASE WHEN t0.salary > t1.average THEN 1.0 ELSE 0.0 END) AS gt
                        FROM tax100w AS t0 LEFT JOIN 
                        (SELECT t2.state, AVG(t2.salary) AS average FROM tax100w AS t2 GROUP BY t2.state) AS t1 
                        ON t0.state=t1.state) AS t3 GROUP BY t3.state 
                        ORDER BY rate DESC LIMIT 2;''').fetchall():
    print(row)
print(f'计算每个州大于平均工资的人比例 {time.time() - start}s')

