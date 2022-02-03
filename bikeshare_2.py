import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june','all']

DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']

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
    city=''
    while True:
        city= input("\n Which city would you like to explore? (Chicago, New York City or Washington)\n").lower()
        if city in CITY_DATA:
            print("\nGot it! Let's explore: ",city)
            break
        else:
            print("\n Please enter a valid city name")

    # get user input for month (january, february, ... , june or all)
    month=''
    while True:
        month = input("\n Which month would you like to consider? (January, February, March, April, May, June)? Type 'all' for no month filter\n").lower()
        if (month in MONTH_DATA) and (month !='all'):
            print("\nThank you. We will filter on: ", month)
            break
        elif (month in MONTH_DATA) and (month =='all'):
            print("\nThank you. We will apply no month filter.")
            break
        else:
            print("\n Please enter a valid month")

    # get user input for day of week (monday, tuesday, ... sunday or all)
    day=''
    while True:
        day = input("\n Which day of the week would you like to consider? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)? Type 'all' for no day filter \n").lower()
        if day in DAY_DATA and day !='all':
            print("\nTHank you. We will filter on: ", day)
            break
        else:
            print("\n Please enter a valid day")

    #print(city, month, day)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) + 1
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print("Start time is {}".format(start_time))

    # display the most common month
    if month != 'all':
        common_month= df['month'].mode()[0]
        months= ['January','February','March','April','May','June']
        common_month= months[common_month-1]
        print("The most Popular month is",common_month)


    # display the most common day of week
    if day !='all':
        common_day= df['day_of_week'].mode()[0]
        days= ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        common_day= days[common_day-1]
        print("The most Popular day is",common_day)

    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    common_start_hour=df['Start Hour'].mode()[0]
    print("The popular Start Hour is {}:00 hrs".format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station= df['Start Station'].mode()[0]
    print("The most commonly used start station is {}".format(common_start_station))

    # display most commonly used end station
    common_end_station= df['End Station'].mode()[0]
    print("The most commonly used end station is {}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    df['combination']=df['Start Station']+" "+"to"+" "+ df['End Station']
    frequent_combination= df['combination'].mode()[0]
    print("The most frequent combination of start and end Station is {} ".format(frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = float (total_travel_time)
    day = total_travel_time // (24 * 3600)
    total_travel_time = total_travel_time % (24 * 3600)
    hour = total_travel_time // 3600
    total_travel_time %= 3600
    minutes = total_travel_time // 60
    total_travel_time %= 60
    seconds = total_travel_time
    print("The total travel time is: " + str(day) + "  days, " + str(hour) + " hours, " + str(minutes) +  " minutes, " + str(seconds)  + " seconds")
    #print("The total travel time is: " + str(total_travel_time) + " seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is: " + str(mean_travel_time) + " seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """
    Displays statistics on bikeshare users.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The count of user types is: \n" + str(user_types) + "\n")

    #Washington file does not include Gender and Birth Year information
    if city != 'washington':
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print("The count of user gender is: \n" + str(gender)+ "\n")
        # Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print('Earliest birth is: {}\n'.format(earliest_birth))
        print('Most recent birth is: {}\n'.format(most_recent_birth))
        print('Most common birth is: {}\n'.format(most_common_birth) )
    else:
        print("sorry the count of user gender is not available for the selected city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Displays raw data on user request.
    """
    row = 0
    view_raw_data=''
    while True:
        if row == 0:
            view_raw_data = input('\nWould you like to view the first five rows of raw data? Enter yes or no.\n')
            if view_raw_data.lower() != 'yes':
                #print("no row data requested")
                return
            print("Below are the first five rows of raw data:")
            row = row + 5
            print(df.iloc[row:row+5])
        else:
            view_raw_data = input('\nWould you like to view the next five rows of raw data? Enter yes or no.\n')
            if view_raw_data.lower() != 'yes':
                #print("no row data requested")
                return
            print("Below are the the next five rows of raw data:")
            row = row + 5
            print(df.iloc[row:row+5])

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
