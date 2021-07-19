import discord
import os
import requests
import json
import random
import datetime
from replit import db
from discord.ext import tasks
from extras import standardErrorMessage, helpText, eventAlerts
from keepalive import keep_alive

client = discord.Client() #this variable represents our bot

#initialize the database where all the infomration about events will be stored
if "remindersInfo" not in db.keys():
  db["remindersInfo"] = {}
if "spamChannel" not in db.keys():
  db["spamChannel"] = 862016512898498594
if "harassmentLevel" not in db.keys():
  db["harassmentLevel"] = 3600

def main():
  
  #print a message once the bot as been successfully loaded
  @client.event
  async def on_ready():
    print("We have logged in as {0}".format(client.user))
    print(datetime.date.today())
    harassment.start()
  
  #loop that harasses people every X seconds, X is 3600 by default but can be changed by users
  @tasks.loop(seconds=db["harassmentLevel"])
  async def harassment():
    channel = client.get_channel(db["spamChannel"])
    yesterday = datetime.date.today() - datetime.timedelta(days = 1)
    eventList = random.choice(eventAlerts)

    #only spam the users if there is at least 1 event in the database
    if len(db["remindersInfo"]) != 0 :

      for reminderEvent in db["remindersInfo"]:
        # if a deadline was yesterday, erase the event associated with it
        if str(yesterday) in db["remindersInfo"][reminderEvent]:
          db["remindersInfo"].pop(reminderEvent)

      eventList = eventList + listOfEventsWithDescription()
      await channel.send(eventList)
          
  @client.event
  async def on_message(message):
    #if a message was sent by the bot, ignore it
    if message.author == client.user:
      return

    msg = message.content
    #this command adds an event, its deadline and (optionally) its description to the databse
    if msg.startswith("%createevent"):

      if len(msg.split(" ",3)) < 3:
        await message.channel.send("Error. Correct usage: %createevent <Title> <Date YYYY-MM-DD> <Description (optional)>." + standardErrorMessage)

      else:
        addEventToDatabase(message)
        eventList = listOfEvents()
        await message.channel.send(eventList)

    #remove a project from the database
    if msg.startswith("%deleteevent"):

      if len(msg.split(" ")) != 2:
        await message.channel.send('Error. Correct usage: %deleteevent <Title> / "All".' + standardErrorMessage)
      
      else:
        #calls a function that will check if the event exists and, if so, delete it
        eventExists = removeEventFromDatabase(message)
        if eventExists:
          eventList = listOfEvents()
          try:
            await message.channel.send(eventList)
          except:
            await message.channel.send("All events have been deleted.")
        else:
          await message.channel.send("Error. Invalid name, could not find " + msg.split(" ")[1] + " in the database." + standardErrorMessage)

    #show a list of all the projects in the database
    if msg.startswith("%eventlist"):
      eventList = listOfEventsWithDescription()
      await message.channel.send(eventList)

    #define which channel should be used to harass users
    if msg.startswith("%definespamchannel"):
      if len(msg.split(" ")) != 2:
        await message.channel.send("Error. Correct usage: %definespamchannel <channel id>." + standardErrorMessage)
      elif not str.isdecimal(msg.split(" ")[1]):
        await message.channel.send("Error. Please input only numeric characters." + standardErrorMessage)
      else:
        db["spamChannel"] = int(msg.split(" ")[1])
        await message.channel.send("Spam channel changed.")

    #change the time between each spam message
    if msg.startswith("%harassmentlevel"):

      if len(msg.split(" ")) != 2:
        await message.channel.send("Error. Correct usage: %mtharassmentlevel small/normal/high/spamoverflow." + standardErrorMessage)
        return

      harassmentLevel = msg.split(" ")[1].lower()
      if harassmentLevel == "small":
        db["harassmentLevel"] = 10800 #3 hours
      elif harassmentLevel == "normal":
        db["harassmentLevel"] = 3600 #1 hour
      elif harassmentLevel == "high":
        db["harassmentLevel"] = 600 #10 minutes
      elif harassmentLevel == "spamoverflow":
        db["harassmentLevel"] = 60 #1 minute
      else:
        await message.channel.send("Error. Invalid input, use small/normal/high/spamoverflow only." + standardErrorMessage)
        return
      harassment.change_interval(seconds=db["harassmentLevel"])
      harassment.restart()
      await message.channel.send("Harassment level changed.")

    #explains users how to use the different commands and what they do
    if msg.startswith("%help"):
      await message.channel.send(helpText)
    #bread puns
    if msg.startswith("%bread"):
      quote = get_quote()
      await message.channel.send(quote)

  keep_alive()
  client.run(os.environ["TOKEN"])

def addEventToDatabase(message):
  msg = message.content
  
  #add the name of the event and its deadline to the database
  reminderDate = msg.split(" ")[2]
  reminderEvent = msg.split(" ")[1].upper()
  db["remindersInfo"][reminderEvent] = [reminderDate]

  #if a description of the event was given as input, add it aswell
  if len(msg.split(" ",3)) == 4:
    eventDescription = msg.split(" ",3)[3]
    db["remindersInfo"][reminderEvent].append(eventDescription)

def removeEventFromDatabase(message):
  msg = message.content
  reminderEvent = msg.split(" ")[1].upper()
  
  #check if the event exists and, if so, delete it 
  if reminderEvent.upper() == "ALL":
    db["remindersInfo"].clear()
    return True
  elif reminderEvent in db["remindersInfo"]:
    db["remindersInfo"].pop(reminderEvent)
    return True
  return False

def listOfEvents():
  eventList = ""
  #add the event title and the its deadline to the list
  for reminderEvent in db["remindersInfo"]:
    eventList = eventList + reminderEvent + " - " + db["remindersInfo"][reminderEvent][0] + "\n"
  return eventList

def listOfEventsWithDescription():
  eventList = ""
  for reminderEvent in db["remindersInfo"]:
    eventList = eventList + reminderEvent + " - " + db["remindersInfo"][reminderEvent][0] + "\n"
    #add a description of the event if it exists
    if len(db["remindersInfo"][reminderEvent]) == 2:
      eventList = eventList + db["remindersInfo"][reminderEvent][1] + "\n"
      
  return eventList

def get_quote():
  response = requests.get("https://my-bao-server.herokuapp.com/api/breadpuns")
  json_data = json.loads(response.text)
  quote = json_data
  return quote

main()
