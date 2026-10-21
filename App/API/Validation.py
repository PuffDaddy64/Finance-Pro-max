"""
 Projet : Finances-Pro-Max
 Directory : API
 Name Of File : Validation.py
 Author : Thomas Raymond
 Author : Félix Roussin
 Date : 17 octobre 2026
 
Description  : Class regrouping all sorts of validation
"""

def IsInteger(number: str) -> bool:
    try:
        int(number)
    except ValueError:
        return False
    except TypeError:
        return False
    return True

def IsYear(year: str):
    if IsInteger(year):
        year_number = int(year)
        if year_number > 0 and year_number < 9999:
            return True
    return False

def IsMonth(month: str):
    if IsInteger(month):
        month_number = int(month)
        if month_number > 0 and month_number < 13:
            return True
    return False

def IsDay(day: str):
    if IsInteger(day):
        day_number = int(day)
        if day_number > 0 and day_number < 32:
            return True
    return False