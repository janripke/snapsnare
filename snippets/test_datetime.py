from datetime import datetime

s = "2020-12-21 23:14:46.805909"
s = datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')
s = s.strftime('%d %B om %H:%M')
print(s)