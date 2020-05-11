## Description
The project is meant to screenscrape apartment data from the main italian real estate websites and send notifications via Telegram to users subscribed to receive apartments upon a given set of restriction preferences (up to 200K€, from 3 rooms, etc.)

The project is composed by 3 main programs:

- _app.py is the scraper entry point to continously crawl data from the configured websites
- _app_bot.py is the Telegram bot which assists a user in setting up his preferences for the apartment he's looking for
- _app_notifier.py acts as a notifier by taking apartments found and sending a Telegram notification to the user of preference

## Prerequisites
Make sure you have installed MySql and Python 3.8.x

## How To Install
After cloning the branch, enter:
`python _config_reset.py`
This will create your database, migrate tables and seed it with data and configurations.

## Technologies
The project is using Python 3.8, MySql, SqlAlchemy for the persistence layer.

## Known Issues
There is an issue since the batch is supposed to run in a multiprocess/multithread environment and some issues come with the database connection.
