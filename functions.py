'''
from datetime import datetime, timedelta
import random

def generate_custom_datetime():
    # Define the start and end datetime strings
    start_datetime_str = '2011-11-24 02:00:01.700000'
    end_datetime_str = '2011-11-24 02:00:01.800000'

    # Convert strings to datetime objects
    start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S.%f')
    end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S.%f')

    # Calculate a random timestamp within the range
    # Generate a random number of microseconds between 0 and 100000 (inclusive)
    random_microseconds = random.randint(0, 100000)

    # Create a timedelta based on the random microseconds
    random_delta = timedelta(microseconds=random_microseconds)

    # Generate a random datetime between start_datetime and end_datetime
    random_datetime = start_datetime + random_delta

    # Return the datetime object formatted in the required format
    return random_datetime.strftime('%Y-%m-%d-%H.%M.%S.%f')

# Example usage
generated_datetime = generate_custom_datetime()
print(generated_datetime)
'''

import random

def generate_random_birthdate():
    # Generate a random year between 1900 and 2023
    year = random.randint(1950, 2023)

    # Generate a random month between 1 and 12
    month = random.randint(1, 12)

    # Generate a random day based on the selected month and year
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:  # February
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            day = random.randint(1, 29)  # Leap year
        else:
            day = random.randint(1, 28)  # Non-leap year

    # Format the generated date as yyyy/mm/dd
    birthdate = f"{year:04}/{month:02}/{day:02}"

    return birthdate

# Example usage
random_birthdate = generate_random_birthdate()
print(random_birthdate)
