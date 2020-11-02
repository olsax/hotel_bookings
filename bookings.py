import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import ticker
from datetime import datetime

pd.options.display.width = None
pd.set_option('max_columns', 10)
#plt.style.use('seaborn')
sns.set_palette("pastel")
sns.set(style='white')

# 'hotel', 'is_canceled' (1-cancelled), 'lead_time' (Number of days that elapsed between the entering date of the booking into the PMS and the arrival date),
#	'arrival_date_year',
#	'arrival_date_month', 'arrival_date_week_number',
#   'arrival_date_day_of_month', 'stays_in_weekend_nights',
#   'stays_in_week_nights', 'adults', 'children', 'babies', 'meal',
#   'country' (ISO 3155–3:2013), 'market_segment' (Market segment designation. In categories, the term “TA” means “Travel Agents” and “TO” means “Tour Operators”),
#	'distribution_channel' (Booking distribution channel. The term “TA” means “Travel Agents” and “TO” means “Tour Operators”),
#   'is_repeated_guest', 'previous_cancellations',
#   'previous_bookings_not_canceled', 'reserved_room_type',
#   'assigned_room_type', 'booking_changes', 'deposit_type',
#	'agent' (ID of the travel agency that made the booking),
#   'company' (ID of the company/entity that made the booking or responsible for paying the booking.),
#	'days_in_waiting_list', 'customer_type', 'adr' (Average Daily Rate),
#	'required_car_parking_spaces', 'total_of_special_requests',
#   'reservation_status', 'reservation_status_date'
# https://www.sciencedirect.com/science/article/pii/S2352340918315191

dataf = pd.read_csv('hotel_bookings.csv')

## numerical attributes
#print(dataf.describe().columns)

missing_data = dataf.isnull().sum()
dataf['children'].fillna(0, inplace=True)

country_data = dataf['country'].value_counts()
dataf['country'].fillna("UNK", inplace=True) #unknown

## categorical/non-numerical attributes
#print([x for x in dataf.columns if x not in dataf.describe().columns])

#dataf_corr = dataf.corr()
#print(dataf_corr['is_canceled'])

## negative correlation so these two columns can be dropped
dataf.drop(['is_repeated_guest', 'previous_bookings_not_canceled', 'required_car_parking_spaces', 'total_of_special_requests', 'booking_changes'], axis=1, inplace=True)
dataf.drop(['agent', 'company'], axis=1, inplace=True)

## put babies and children together
dataf['children'] = dataf['children'] + dataf['babies']
dataf.drop(['babies'], axis=1, inplace=True)

sns.countplot(x='hotel', data=dataf, hue='is_canceled', palette='pastel')
#plt.show()

dataf['stays_in_nights'] = dataf['stays_in_weekend_nights'] + dataf['stays_in_week_nights']

dataf['arrival_date'] = dataf['arrival_date_day_of_month'].astype(str) + '-' + dataf['arrival_date_month'] + '-' + dataf['arrival_date_year'].astype(str)
dataf['arrival_date'] = dataf['arrival_date'].apply(pd.to_datetime, format='%d-%B-%Y')
dataf.drop(['arrival_date_day_of_month', 'arrival_date_week_number', 'arrival_date_month', 'arrival_date_year'], axis=1, inplace=True)

dataf['reservation_status_date'] = dataf['reservation_status_date'].apply(pd.to_datetime, format='%Y-%m-%d')

dataf['canc_to_arrival_days'] = (dataf['arrival_date'] - dataf['reservation_status_date']).dt.days
dataf['canc_to_arrival_days'] = np.where(dataf['reservation_status'] == 'Canceled', dataf['canc_to_arrival_days'], -1)

ax = sns.displot(dataf['lead_time'], bins=np.arange(0,dataf['lead_time'].max(),50), kde=False, height=4, aspect=2)
ax.set(xlabel="lead time to the arrival date")
#plt.show()

tempdf = dataf[dataf['canc_to_arrival_days'] != -1]

ax = sns.displot(tempdf['canc_to_arrival_days'], kde=True, color="purple", height=4, aspect=2)
ax.set(xlabel="days between cancellation and booked date", ylabel=" ")
plt.xlim(xmin=0)
#plt.show()

#print(dataf.columns.values)
#print(dataf['market_segment'].count)
#print(tempdf['market_segment'].count)

#for discrete values - months
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
g = sns.countplot(x=dataf['arrival_date'].dt.month, data=dataf, palette='pastel')
g.set_xticklabels(months)
plt.title('number of cancellations in each of the months')
plt.xticks(rotation = 90)
#plt.show()


## for market segment
# Count Plot (a.k.a. Bar Plot)
sns.countplot(x='Type 1', data=df, palette=pkmn_type_colors)
 
# Rotate x-labels
plt.xticks(rotation=-45)