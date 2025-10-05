import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city
    valid_cities = ['chicago', 'new york city', 'washington']
    city = input("What is the city that you want to learn about? ").lower()
    while city not in valid_cities:
        print("Invalid city. Please choose Chicago, New York City, or Washington.")
        city = input("What is the city that you want to learn about? ").lower()
    print("You selected:", city)

    # get user input for month
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input("Which month you want to know about? (all, january, february, ... , june): ").lower()
    while month not in valid_months:
        print("Invalid month. Please choose all, january, february, march, april, may, or june.")
        month = input("Which month you want to know about? ").lower()

    # get user input for day of week
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input("Which day you want to know about? (all, monday, tuesday, ... sunday): ").lower()
    while day not in valid_days:
        print("Invalid day. Please choose all, monday, tuesday, wednesday, thursday, friday, saturday, or sunday.")
        day = input("Which day you want to know about? ").lower()

    if day != 'all':
        day = day.title()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month) + 1
        df = df[df['month'] == month_num]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # most common month
    common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('The most common month is:', months[common_month - 1])

    # most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of week is:', common_day)

    # most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most common start hour is:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # most common start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is:', common_start_station)

    # most common end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is:', common_end_station)

    # most common trip combination
    common_trip = (df['Start Station'] + " -> " + df['End Station']).mode()[0]
    print('The most common trip is:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # total travel time
    travel_time = df['Trip Duration'].sum()
    print('The total travel time is:', travel_time)

    # mean travel time
    travel_mean = df['Trip Duration'].mean()
    print('The average travel time is:', travel_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # counts of user types
    count_user_type = df['User Type'].value_counts()
    print('The count of user types is:\n', count_user_type)

    # counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nThe gender count is:\n', gender_counts)
    else:
        print('\nGender data is not available for this city.')

    # birth year stats
    if 'Birth Year' in df.columns:
        most_recent = int(df['Birth Year'].max())
        earliest = int(df['Birth Year'].min())
        most_common = int(df['Birth Year'].mode()[0])

        print('\nEarliest year of birth:', earliest)
        print('Most recent year of birth:', most_recent)
        print('Most common year of birth:', most_common)
    else:
        print('\nBirth year data is not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays raw data 5 rows at a time upon user request."""
    start_row = 0
    show_data = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n').lower()

    while show_data == 'yes' and start_row < len(df):
        print(df.iloc[start_row:start_row+5])
        start_row += 5
        show_data = input('\nWould you like to see 5 more rows of raw data? Enter yes or no.\n').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
