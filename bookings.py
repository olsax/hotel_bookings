import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

pd.options.display.width = None
pd.set_option('max_columns', 8)
plt.style.use('seaborn')

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
print(dataf.head())

# numerical attributes
#print(dataf.describe().columns)

#num_atr = dataf.select_dtypes(include=['int'])
#num_atr = dataf.describe().columns
#for col in num_atr: 
#	plt.hist(dataf[col], alpha=0.5)
#	plt.show()

missing_data = dataf.isnull().sum()
dataf['children'].fillna(0, inplace=True)

country_data = dataf['country'].value_counts()
dataf['country'].fillna("UNK", inplace=True) #unknown


#dataf.drop(['agent', 'company'], axis=1, inplace=True)
#categorical/non-numerical attributes
#print([x for x in dataf.columns if x not in dataf.describe().columns])

#sns.countplot(x='hotel', data=dataf, hue='is_canceled', palette='pastel')
#plt.show()

dataf_corr = dataf.corr()

#negative correlation so these two columns can be dropped
dataf.drop(['is_repeated_guest', 'previous_bookings_not_canceled', 'required_car_parking_spaces', 'total_of_special_requests', 'booking_changes'], axis=1, inplace=True)

#put babies and children together
dataf['children'] = dataf['children'] + dataf['babies']
dataf.drop(['babies'], axis=1, inplace=True)

dataf['nights_in'] = dataf['stays_in_weekend_nights'] + dataf['stays_in_week_nights']
dataf_corr = dataf.corr()
print(dataf_corr['is_canceled'])

sns.set_palette("pastel")
sns.displot(dataf['lead_time'], bins=np.arange(0,dataf['lead_time'].max(),25), kde=False, height=4, aspect=2)
plt.show()