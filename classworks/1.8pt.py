n = int (input ())
hour = n // 60
if hour >= 24:
    k = hour // 24
    hour = hour - k * 24
minute = n % 60
print (hour, minute)
