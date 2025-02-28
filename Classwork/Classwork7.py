"""
Name: Jose Miguel Ortiz
Email: jose.ortiz60@lagcc.cuny.edu
Pod:
Date: 02/27/2025

"""

if __name__ == '__main__':

    import pandas as pd
    import matplotlib.pyplot as plt

    mta = pd.read_csv('2020-si-ridership.csv')
    mta['date'] = pd.to_datetime(mta['date'])
    mta = mta.sort_values('date')
    mta['30DayRolling'] = mta['entries'].rolling(30).mean()
    mta['CumulativeAvg'] = mta['entries'].expanding().mean()
    mta['Today'] = mta['entries']
    mta['WeekAgo'] = mta['entries'].shift(7)      # 7 days prior
    mta['TwoWeeksAgo'] = mta['entries'].shift(14) # 14 days prior

    plt.figure(figsize=(12, 6))
    plt.plot(mta['date'], mta['entries'], label='Daily Entries', alpha=0.5)
    plt.plot(mta['date'], mta['30DayRolling'],
             label='30-Day Rolling Avg', color='red', linewidth=2)

    plt.title('MTA Ridership with Rolling Average (Staten Island 2020)')
    plt.ylabel('Number of Riders')
    plt.xlabel('Date')

    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()