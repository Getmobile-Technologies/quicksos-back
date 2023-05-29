from datetime import datetime, time, timedelta
from django.utils import timezone


def get_start_end_of_day(start_date_str, end_date_str):
    """Given the start and end date, return the start of day and end of day for filtering within the application's timezone"""
    
    target_tz = timezone.get_current_timezone()
    
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    
    target_date = timezone.datetime(start_date.year, start_date.month, start_date.day, tzinfo=target_tz)
    start_of_day = datetime.combine(target_date, time.min).astimezone(target_tz)
    
    target_date = timezone.datetime(end_date.year, end_date.month, end_date.day, tzinfo=target_tz)
    end_of_day = datetime.combine(target_date, time.max).astimezone(target_tz)
    
    return start_of_day, end_of_day



def get_month(target_month, target_year):
    
    """Returns start and end of a specific month in a year"""
    
    target_tz = timezone.get_current_timezone()
    
    # Set the start date to the beginning of the target month
    start_date = datetime(target_year, target_month, 1).date()

    # Calculate the end date as the beginning of the next month, then subtract one day to get the last day of the target month
    end_date = (datetime(target_year, target_month + 1, 1) - timedelta(days=1)).date()

    target_date = timezone.datetime(start_date.year, start_date.month, start_date.day, tzinfo=target_tz)
    start_of_mth = datetime.combine(target_date, time.min).astimezone(target_tz)
    
    target_date = timezone.datetime(end_date.year, end_date.month, end_date.day, tzinfo=target_tz)
    end_of_mth = datetime.combine(target_date, time.max).astimezone(target_tz)

  
    print(start_of_mth, end_of_mth)
    return start_of_mth, end_of_mth