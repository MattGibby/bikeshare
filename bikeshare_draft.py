import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    print('\nHello! Let\'s explore some US bikeshare data!')

    cities = ['Chicago', 'Washington', 'New York']
    city = ""
    while city not in cities:
        city = input('\nWould you like to see data for Chicago, New York, or Washington?\n').title()
        if city in cities:
            print('\n{}. Nice choice!'.format(city))
            break
        else:
            print('\nCity not recognised. Please try again.\n')

    filters = ['Month', 'Day', 'None']
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    filt = ""
    month = ""
    day = ""
    while filt not in filters:
        filt = input('\nWould you like to filter the data by month, day, or not at all? \nType "no" for no time filter.\n').title()
        if filt == 'No':
            month = 'all'
            day = 'all'
            print ('\nCalculating full period stats for {}...'.format(city))
            break
        elif filt == 'Month':
            month = input('\nWhich month please? January, February, March, April, May or June?\n').title()
            day = 'all'
            print ('\nCalculating stats for {} in {}...'.format(city, month))
            break
        elif filt == 'Day':
            month = 'all'
            day = input('\nWhich day please? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n').title()
            print ('\nCalculating stats for {} on {}s...'.format(city, day))
            break
        else:
            print('\nFilter not recognised. Please try again.\n')

    print('-'*40)
    return city, month, day

def load_data(city, month, day):

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].value_counts()
    pm_index = popular_month.index[0]
    pm_values = popular_month.values[0]
    print('\nMost common month: {} (count {})'.format(pm_index, pm_values))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].value_counts()
    pd_index = popular_day.index[0]
    pd_values = popular_day.values[0]
    print('\nMost common day of week: {} (count {})'.format(pd_index, pd_values))

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].value_counts()
    ph_index = popular_hour.index[0]
    ph_values = popular_hour.values[0]
    print('\nMost common start hour: {} (count {})'.format(ph_index, ph_values))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_stn = df['Start Station'].value_counts()
    pss_index = popular_start_stn.index[0]
    pss_values = popular_start_stn.values[0]
    print('\nMost common start station: {} (count {})'.format(pss_index, pss_values))

    # TO DO: display most commonly used end station
    popular_end_stn = df['End Station'].value_counts()
    pes_index = popular_end_stn.index[0]
    pes_values = popular_end_stn.values[0]
    print('\nMost common end station: {} (count {})'.format(pes_index, pes_values))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start_End_Stations'] = df['Start Station'] +  ' / ' + df['End Station']
    popular_trip = df['Start_End_Stations'].value_counts()
    pt_index = popular_trip.index[0]
    pt_values = popular_trip.values[0]
    print('\nMost common start and end stations: {} (count {})'.format(pt_index, pt_values))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal travel time: {} seconds'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time: {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print('\nCount of user types: \n{}'.format(user_types))

    # TO DO: Display counts of gender
    if city != 'Washington':
        gender = df['Gender'].value_counts().to_frame()
        print('\nCount of gender: \n{}'.format(gender))
    else:
        print('\nNo gender data available for Washington')

    # TO DO: Display earliest, most recent, and most common year of birth
    if city != 'Washington':
        birth_year_earliest = df['Birth Year'].min()
        print('\nEarliest year of birth: {}'.format(int(birth_year_earliest)))
        birth_year_latest = df['Birth Year'].max()
        print('\nLatest year of birth: {}'.format(int(birth_year_latest)))
        birth_year = df['Birth Year'].value_counts()
        by_index = int(birth_year.index[0])
        by_values = birth_year.values[0]
        print('\nMost common year of birth: {} (count {})'.format(by_index, by_values))
    else:
        print('\nNo birth year data available for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
