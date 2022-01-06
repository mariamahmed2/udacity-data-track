import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


def checkData(data):
    cites = ['chicago','new york city','washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june','all']
    days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']

    while 1:
        temp = input(data).lower()
        try:
           if temp in cites:
              break

           elif temp in months:
               break

           elif temp in days:
             break
           else:
               if temp not in cites:
                   print('Enter a valid city')
               if temp not in months:
                   print('Enter a valid month')
               if temp not in days:
                  print('Enter a valid day')
        except ValueError:
            print("Erorr")

    return temp


# function to display the data
def display_data(city):
    while True:
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
        start_loc = 0
        if city == 'chicago':
            df = pd.read_csv('chicago.csv')
        elif city == 'new york city':
            df = pd.read_csv('new_york_city.csv')
        else:
            df = pd.read_csv('washington.csv')
        while (view_data == 'yes'):
            print(df.iloc[start_loc: start_loc + 5])
            start_loc += 5
            view_display = input("Do you wish to continue?: ").lower()
            if view_display == 'yes':
                continue
            elif view_display == 'no':
                break
        break



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
    city = checkData('Choose the city\n')
    display_data(city)

    # get user input for month (all, january, february, ... , june)
    month = checkData('Set the month\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = checkData('Set the day\n')

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

    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month

    # extract day_of_week from the Start Time column to create a day_of_week column
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

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
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mostMonth = df['month'].mode()[0]
    print(f'The most popular month : {mostMonth}')

    # display the most common day of week
    mostDay = df['day_of_week'].mode()[0]
    print(f'The most common day : {mostDay.title()}')

    # display the most common start hour
    mostHour = df['hour'].mode()[0]
    print(f'Most common start hour: {mostHour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    startStation = df['Start Station'].mode()[0]
    print('The most commonly used start station:', startStation)

    # display most commonly used end station
    endStation = df['End Station'].mode()[0]
    print('The most commonly used end station:', endStation)

    # display most frequent combination of start station and end station trip
   # commonStart = df['Start Station'].value_counts()[startStation]
    #commonEnd = df['End Station'].value_counts()[endStation]

    startEnd = (df['Start Station'] + "to" + df['End Station']).mode()[0]
    print(f'Most frequent start and end station :', startEnd)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    totalTime = df['Trip Duration'].sum()
    print('The total travel time is: ', totalTime)

    # display mean travel time
    meanTime = df['Trip Duration'].mean()
    print('The mean travel time is: ', meanTime)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    userType = df['User Type'].value_counts()
    print('The counts of user types: ', userType)

    if city == 'chicago.csv' or city == 'new_york_city.csv':
        #Display counts of gender
        gender = df['Gender'].value_counts()
        print('The count of user gender: ', gender)

        # Display earliest, most recent, and most common year of birth
        earliestBirth = df['Birth Year'].min()
        print('The Earliest birth :',earliestBirth)

        recentBirth = df['Birth Year'].max()
        print('The most recent birth :',recentBirth)

        mostBirth = df['Birth Year'].mode()[0]
        print('The most common birth :',mostBirth)

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