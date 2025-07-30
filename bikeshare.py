import time
import pandas as pd
import numpy as np

""" 
This section creates the mapping used to read in the datasets and map the user filter inputs.

"""
CITY_DATA = {'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv'}
months = {'january', 'february', 'march', 'april', 'may', 'june', 'all'}
day_map = {'1': 'Sunday','2': 'Monday','3': 'Tuesday','4': 'Wednesday','5': 'Thursday','6': 'Friday','7': 'Saturday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid input. Please enter either Chicago, New York, or Washington.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to see data for? (January, February, March, April, May, June, or all.)").strip().lower()
        if month in months:
            break
        else:
            print('Invalid input. Please enter either January, February, March, April, May, June, or all.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day of the week would you like data for? (Please type your response as an integer: 1 = Sunday, 7 = Saturday. For every day, type all.)")
        if day in day_map or day == 'all':
            break
        else:
            print('Invalid input. Please type your response as an integer: 1 = Sunday, 7 = Saturday. For every day, type all.')

    print('-'*40)

    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day_name = day_map.get(day)
        if day_name:
            df = df[df['day_of_week'] == day_name]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print(f'The most popular month is {popular_month}')

    # display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print(f'The most popular day is {popular_day}')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f'The most popular hour is {popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f'The most popular hour is {popular_start_station}')

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f'The most popular hour is {popular_end_station}')

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " -> " + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print(f'The most popular trip is {popular_trip}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'The total travel time was {total_travel_time}')

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print(f'The average travel time was {average_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users. Users simply hit enter to continue to view data."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts(dropna=True)
    print(f'Here are the counts of the different user types: {user_types}')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts(dropna=True)
        print(f'Here are the counts of each gender: {gender_types}')
    else:
        print('Gender data is not available.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_years = df['Birth Year'].dropna()
        if not birth_years.empty:
            oldest = int(birth_years.min())
            youngest = int(birth_years.max())
            popular_age = int(birth_years.mode()[0])
            print(f'The earliest year of birth was {oldest}')
            print(f'The most recent year of birth was {youngest}')
            print(f'The most common year of birth was {popular_age}')
    else:
        print('Birth year data not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    view_data = input('Would you like to view 5 rows of individual trip data? Enter yes or no.').strip().lower()
    start_loc = 0

    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input('Do you wish to continue? Enter yes or no: ').strip().lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()