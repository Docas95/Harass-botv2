# Harass-botv2

## A bot to remind everyone in your discord server of... anything you'd like really!
This was my very first project, so it's nothing amazing, but I'm still very proud of it!

## How does it work:
Once the bot has been added to any server of your choice, all you have to do is use the bot commands to insert an event you want everyone in your discord server to be reminded of into the bot's database and define which channel should be used to remind people of the event. After that, the bot will send a notification to everyone in the server every X minutes as a reminder of the event. Once the deadline of the event is met, the project will be deleted automatically.

Events can be added or removed from the database at any time, users can request to see a list of all the available events at any time aswell.

The amount of time between each reminder can be changed, you could send everyone a notification every minute, the bot isn't called "harass-bot" for no reason!

## Examples:

![Adding an event to the bot by using "%createevent"](https://user-images.githubusercontent.com/61094301/126234900-56c2d86d-9ced-46be-8c00-a70b85c7d92c.png)

![Requesting to see a list of all the available events by using "%eventlist"](https://user-images.githubusercontent.com/61094301/126234930-ab188bad-7481-438b-b051-93388643dc38.png)

![Example of Harass-bot's reminders](https://user-images.githubusercontent.com/61094301/126234977-402fe565-0d5a-48fb-88ee-641e0e546d62.png)

# How to use:
Use this link to invite this bot to your server: https://discord.com/api/oauth2/authorize?client_id=862079199560728606&permissions=2148001856&scope=bot

Type "%help" in any channel and the bot will show how to use all of its commands.

## External Packages used:

- discord.py
- requests
- json
- replit

All built in python!

