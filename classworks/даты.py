
#Три числа - год, месяц, день; return True если есть в календаре, False - нет

def data (year, month, day):
    if month > 12:
        return False
    else:
        if day >= 31:
            return False
        else:
            if day == 31 and (month == 2 or month == 4 or month == 9 or month == 11 or month == 6):
                return False
            else:
                if day == 30 and month == 2:
                    return False
                else:
                    if day == 29 and month == 2 and (year % 4 != 0 or (year % 100 == 0 and year % 1000 != 0)):
                        return False
                    elif day == 16 and month == 12 and year == 1998:
                        print ("Вы угадали день рождения разработчика! Не забудьте его поздравить :)")
                    else:
                        return True
year = input ("Введите год (натуральное число): ")
month = input ("Введите месяц (натуральное число до 12 включительно): ")
day = input ("Введите день (натуральное число до 31 включительно): ")
while year and month and day:
    if data (int(year), int(month), int(day)) == True:
        print ("Такая дата есть в календаре:)")
    elif data (int(year), int(month), int(day)) == False:
        print ("Простите, но такой даты нету:(")
    else:
        print (data (int(year), int(month), int(day)))
    print ("Попробуем снова:)")
    year = input ("Введите год (натуральное число): ")
    month = input ("Введите месяц (натуральное число до 12 включительно): ")
    day = input ("Введите день (натуральное число до 31 включительно): ")
print ("Все!:)")

    
