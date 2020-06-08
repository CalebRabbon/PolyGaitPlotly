import json
import sys
import datetime
import csv
import sqlite3
from pozyxpoint import PozyxPoint
from tag import Tag

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("""CREATE TABLE pozyxpoint (
            x real,
            y real,
            z real,
            timestamp real
            )""")

def insert_pozyxpoint(pt):
    with conn:
        c.execute("INSERT INTO pozyxpoint VALUES (:x, :y, :z, :t)", {'x': pt.x, 'y': pt.y, 'z': pt.z, 't': pt.timestamp})


def findAvgLocation(loc):
   xAvg = 0
   yAvg = 0
   zAvg = 0
   tAvg = 0
   elements = 0

   x = 0
   y = 1
   z = 2
   t = 3

#  Find totals
   for l in loc:
      print(l)
      elements += 1
      xAvg += l[x]
      yAvg += l[y]
      zAvg += l[z]
      tAvg += l[t]

   if(elements == 0):
      return PozyxPoint(0, 0, 0, 0)

   print(elements)

   xAvg = xAvg / elements
   yAvg = yAvg / elements
   zAvg = zAvg / elements
   tAvg = tAvg / elements

   return PozyxPoint(xAvg, yAvg, zAvg, tAvg)

# Finds the average location of the input timestamp with in +/- .75 seconds of the input timestamp
# Returns a PozyxPoint
def get_position(timestamp):
   locations = []
   c.execute("SELECT * FROM pozyxpoint WHERE abs(timestamp-:t) <= .75", {'t': timestamp})
   locations = c.fetchall()
   return findAvgLocation(locations)


def remove_pozyxpoint(timestamp):
    with conn:
        c.execute("DELETE from pozyxpoint WHERE timestamp= :t", {'t': pozyxpoint.timestamp})


def getTimeStamp(line):
   dateArr = []
   timeArr = []
   date = line[2]
   time = line[3]

   dateArr = date.split('-', 2)
   year = int(dateArr[0])
   month = int(dateArr[1])
   day = int(dateArr[2])

   timeArr = time.split(':', 2)
   hour = int(timeArr[0])
   minute = int(timeArr[1])
   second = int(timeArr[2])

   #print("year " + str(year) + " month "+  str(month) + " day " + str(day) + " time: " + time)
   # We may need to change the timezone but not sure - Caleb Rabbon 6/7/2020
   timestamp = datetime.datetime(int(year), month, day, hour, minute, second).timestamp()
   #print(timestamp)
   return timestamp

def getID(line):
    return line[0]

# Creates a list of tags from a ministock .csv file
def createTagList(filename):
   tagList = []

   with open(filename, 'r') as csv_file:
      csv_reader = csv.reader(csv_file)

      # Skip the header of the csv file
      next(csv_reader)

      for line in csv_reader:
         date = line[2]
         time = line[3]
         tagID = getID(line)
         timestamp = getTimeStamp(line)
         tag = Tag(tagID, date, time, timestamp)
         tagList.append(tag)

   return tagList

def createPozyxPoints(filename):
   json_data = []
   coor = []

   jsonfile = open(filename, 'r')
   for line in jsonfile:
         json_line_list = json.loads(line)
         json_line = json_line_list[0]
         tag = json_line["tagId"]
         timestamp = json_line["timestamp"]
         xmm = json_line["data"]["coordinates"]["x"]
         ymm = json_line["data"]["coordinates"]["y"]
         zmm = json_line["data"]["coordinates"]["z"]

         # Convert coordiates from mm to inches
         xinch = xmm * .0393701
         yinch = ymm * .0393701
         zinch = zmm * .0393701

         # Convert coordinates from inches to feet
         xfeet = xinch / 12
         yfeet = yinch / 12
         zfeet = zinch / 12
         pt = PozyxPoint(xfeet, yfeet, zfeet, timestamp)

#         coor.append([xfeet, yfeet, zfeet, timestamp])
         coor.append(pt)

   # Closing jsonfile
   jsonfile.close()

   return coor

# Takes in a tagList and the coordinates list and returns a final list of tuples representing the tag and its position
def findAllPositions(tagList, coordinates):
   finalList = []

   # Fill in the coordinate database
   for val in coordinates:
      insert_pozyxpoint(val)
      print(val)

   for tag in tagList:
      pt = get_position(tag.getTimestamp)
      finalList.append([tag, pt])

   return finalList

def checkArgs():
   if len(sys.argv) != 3:
      sys.exit("Usage Error: Not enough arguments \nExample Run: python finalGraph.py ministock.csv test.json")

def main():
   checkArgs()
   tagList = []
   coordinates = []

   # Contains a tuple of tag and position
   finalList = []

   # Creates the list of tags from the ministock
   tagList = createTagList(sys.argv[1])

   # Creates a list of PozyxPoint objects
   coordinates = createPozyxPoints(sys.argv[2])

   finalList = findAllPositions(tagList, coordinates)

   for e in finalList:
      print(e)

   conn.close()

if __name__== "__main__":
   main()
