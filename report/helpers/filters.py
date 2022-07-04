from datetime import datetime

def filter_results(data, key:datetime):
    """Function to filter the data in the array by a given key."""
    
   
    return list(filter(lambda x: key >= x["date_created"], data))