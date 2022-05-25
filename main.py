import usd_rate as usd
import datetime as dt
import schedule
import time
import gs_handler as gs
import db_handler as db





# Get current CBRF usd-to-rub rate
# from 'https://www.cbr.ru/scripts/XML_daily.asp'
current_usd_rate = usd.get_rate()
print(f'{dt.datetime.now()}: 1 USD = {current_usd_rate} RUB')

# Grab initial data for population db
data = gs.fetch_all_data(current_usd_rate)
# print(data)

# Create table if not exists
db.create_table_if_not_exist()

# Clear out of date data from the table before insertion
db.delete_from_table()

# Populate DB with initial data
db.insert_into_table(data)

# Check USD rate changes
def check_usd_rate():
    global current_usd_rate
    new_usd_rate = usd.get_rate()
    if current_usd_rate != new_usd_rate:
        current_usd_rate = new_usd_rate
        print(f'{dt.datetime.now()}: 1 USD = {current_usd_rate} RUB')
        return

# Check data changes
def check_data_update():
    global data

    new_data = gs.fetch_all_data(current_usd_rate)
    if data == new_data:
        print(f'{dt.datetime.now()}: no changes')
    else:
        print(f'{dt.datetime.now()}: some changes detected')
        db.delete_from_table()


        # Synchronize global variable data with new data
        data = new_data
        db.insert_into_table(data)
        print(f'{dt.datetime.now()}: ...db updated')


# Update ust-to-rub rate. Target is 00:01 Moscow TZ,
# but due to simplify summer-winter time changes,
# weekends and holidays it pings hourly at XX:01 (min)
schedule.every().hour.at(":01").do(check_usd_rate)

# Google sheet data inspection, run minutely at XX:10 (sec)
# to avoid collision with updated usd rate
schedule.every().minute.at(":10").do(check_data_update)


while True:
    schedule.run_pending()
    time.sleep(1) # wait one minute