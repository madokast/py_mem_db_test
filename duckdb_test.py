import duckdb
import time

db = duckdb.connect(':memory:')

start = time.time()
db.read_csv('tax100w.csv', header=True, dtype={'salary':'float', 'rate':'float', 'singleexemp':'float', 'marriedexemp':'float', 'childexemp': 'float'})
db.sql("CREATE VIEW tax100w AS SELECT * FROM 'tax100w.csv';")
print(f'read csv {time.time() - start}s')

#  表长度计算
start = time.time()
db.sql("SELECT COUNT(1) FROM tax100w").show()
print(f'SELECT COUNT(1) {time.time() - start}s')

# 表前 10 行
# start = time.time()
# db.sql("SELECT * FROM tax100w LIMIT 10").show()
# print(f'SELECT COUNT(1) {time.time() - start}s')

# 计算每个州的平均工资
# SELECT state, AVG(salary) FROM tax100w GROUP BY state
start = time.time()
db.sql('SELECT state, AVG(salary) as average FROM tax100w GROUP BY state ORDER BY average DESC LIMIT 2').show()
print(f'计算每个州的平均工资 {time.time() - start}s')

# 计算每个州大于平均工资的人比例
start = time.time()
db.sql('''SELECT t3.state, SUM(t3.gt) / COUNT(t3.gt) AS rate FROM 
        (SELECT t0.state, (CASE WHEN t0.salary > t1.average THEN 1.0 ELSE 0.0 END) AS gt 
        FROM tax100w AS t0 LEFT JOIN 
        (SELECT t2.state, AVG(t2.salary) AS average FROM tax100w AS t2 GROUP BY t2.state) AS t1 
        ON t0.state=t1.state) AS t3 GROUP BY t3.state 
        ORDER BY rate DESC LIMIT 2''').show()
print(f'计算每个州大于平均工资的人比例 {time.time() - start}s')