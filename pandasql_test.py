import pandas as pd
import pandasql as ps
import time

start = time.time()
tax100w = pd.read_csv('tax100w.csv', dtype={'salary':float, 'rate':float, 'singleexemp':float, 'marriedexemp':float, 'childexemp': float})
print(f'read csv {time.time() - start}s')

# 展示数据
start = time.time()
print('table length\n', ps.sqldf('SELECT COUNT(1) FROM tax100w', locals()))
print(f'SELECT COUNT(1) {time.time() - start}s')


# 计算每个州的平均工资
# SELECT state, AVG(salary) FROM tax100w GROUP BY state
start = time.time()
print(ps.sqldf('SELECT state, AVG(salary) average FROM tax100w GROUP BY state ORDER BY average DESC LIMIT 2', locals()))
print(f'计算每个州的平均工资 {time.time() - start}s')

# 计算每个州大于平均工资的人比例
start = time.time()
print(ps.sqldf('''SELECT t3.state, SUM(t3.gt) / COUNT(t3.gt) AS rate FROM 
                (SELECT t0.state, (CASE WHEN t0.salary > t1.average THEN 1.0 ELSE 0.0 END) AS gt
                FROM tax100w AS t0 LEFT JOIN 
                (SELECT t2.state, AVG(t2.salary) AS average FROM tax100w AS t2 GROUP BY t2.state) AS t1 
                ON t0.state=t1.state) AS t3 GROUP BY t3.state
                ORDER BY rate DESC LIMIT 2;''', locals()))
print(f'计算每个州大于平均工资的人比例 {time.time() - start}s')