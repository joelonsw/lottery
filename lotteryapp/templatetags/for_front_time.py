from django import template

register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return int (value / arg)
    except (ValueError, ZeroDivisionError):
        return None
        
@register.filter
def modulo(value, arg):
    try:
        return int (value % arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter
def hour(value):
    print(value)
    return int(value/3600)

@register.filter
def minute(value):
    hour = int(value/3600)
    min = value-hour*3600
    return int(min/60)

@register.filter
def second(value):
    hour = int(value/3600)
    minute = value-hour*3600
    return minute-((int(minute/60))*60)

@register.filter
def hms(value):
    hour = int(value/3600)
    minute = int((value-hour*3600)/60)
    second = value-(hour*3600)-(minute*60)
    print(hour, minute, second)
    if(hour<10):
        strhour = "0"+str(hour)
    else:
        strhour = str(hour)
    if(minute<10):
        strminute = "0"+str(minute)
    else:
        strminute = str(minute)    
    if(second<10):
        strsecond = "0" + str(second)
    else:
        strsecond = str(second)
    retval = strhour + ":" + strminute + ":" + strsecond
    return retval