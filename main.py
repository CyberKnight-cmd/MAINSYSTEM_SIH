import math
from datetime import datetime
import pandas as pd
import csv
from Reciever import processedString
from NewUserRegistration import requestNew, User
import os
import time

class Employee:

    CSV_FILE = ""
    def __init__(self, user_id, hash, latitude, longitude) -> None:
        self.user_id = user_id
        self.hash = hash
        self.latitude = float(latitude)
        self.longitude= float(longitude)
        currentDirectory = os.path.join(os.getcwd(), 'database')
        for root, dirs, files in os.walk(currentDirectory):
            for file in files:
                if file.startswith(user_id):
                    self.CSV_FILE = os.path.join(root, file)
                    print(self.CSV_FILE)
        if(self.CSV_FILE==""):
            if input(f"No records found for User-Id : {self.user_id}. \nWould you like to create one?\nEnter (y/n) : ") == 'y' :
                if not User.isUserPresent(self.user_id):
                   self.user_id = User.addEntry(nameOfTheUser=input("Please enter the name of the user : "), email = input("Please enter the user's email Address : "))
                   User.addHashCode(self.user_id, self.hash)
                file_name = self.user_id + '_' + User.getName(self.user_id) + '.csv'
                self.CSV_FILE = os.path.join(currentDirectory, file_name)
                with open(self.CSV_FILE, "a") as file:
                    # Write to the file
                    file.write("user_id,hash,latitude,longitude,date_time,distance,category\n")
        
        with open(self.CSV_FILE, "a") as file:
            distances = self.calculateRadius(self.latitude,self.longitude)
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_type = self.timeTypeDeclaration(distances, current_datetime)
            file.write(f"{self.user_id},{self.hash},{self.latitude},{self.longitude},{current_datetime},{min(distances):.2f},{time_type}\n")
    
    def calculateRadius(self, latitude, longitude):
    # First location is main site (for now it is of UEM)
    # Rest are off sites
    #(latitude, longitude)
        locations = [(22.559836,88.490211),(22.699831,88.374534),(22.589607,88.390643)]
        distances = []
        for location in locations:
            dlat = abs(location[0] - latitude)
            dlong = abs(location[1] - longitude)
            # Calculate the Haversine distance
            a = math.sin(dlat/2)**2 + math.cos(latitude) * math.cos(location[0]) * math.sin(dlong/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

            # Calculate the distance in meters using Earth's radius
            distance = 6371000 * c
            distances.append(distance)
        return distances
    def timeTypeDeclaration(self, distances, current_datetime):
        min_distance = min(distances)
        if min_distance < 200:
            # Read the CSV file to determine the time type
            with open(self.CSV_FILE, "r") as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                if len(rows) == 0:
                    # First entry of the day, it's a check-in
                    time_type = "check-in"
                else:
                    last_row = rows[-1]
                    last_time_type = last_row["category"]
                    current_date = current_datetime.split(" ")[0]
                    last_date = last_row["date_time"].split(" ")[0]
                    last_time = datetime.strptime(last_row["date_time"], "%Y-%m-%d %H:%M:%S")
                    time_diff = (datetime.strptime(current_datetime, "%Y-%m-%d %H:%M:%S") - last_time).total_seconds() / 60
                    if current_date != last_date:
                        # New day, it's a check-in
                        time_type = "check-in"
                    elif time_diff > 25:
                        # Entry is older than 25 minutes, declare it dead and last signal as checkout
                        with open(self.CSV_FILE, "r") as file:
                            reader = csv.DictReader(file)
                            rows = list(reader)
                            last_row = rows[-1]
                            last_row["category"] = "check-out"
                        with open(self.CSV_FILE, "w") as file:
                            writer = csv.DictWriter(file, fieldnames=last_row.keys())
                            writer.writeheader()
                            for row in rows[:-1]:
                                writer.writerow(row)
                            writer.writerow(last_row)
                        # Add a new entry as a check-in
                        with open(self.CSV_FILE, "a") as file:
                            file.write(f"{self.user_id},{self.hash},{self.latitude},{self.longitude},{current_datetime},{min(distances):.2f},check-in\n")
                        time_type = "check-in"
                    elif last_time_type == "check-in":
                        # Already checked-in, it's a confirmation
                        time_type = "confirmation"
                    else:
                        # Last entry was a check-out, it's a check-in
                        time_type = "check-in"
        else:
            # Distance exceeded, it's a check-out
            time_type = "check-out"
        return time_type


if __name__ == '__main__':
    file_path = "bufferlist.txt"
    with open(file_path, "r+") as file:
        buffer_list = file.readlines()
        for line in buffer_list:
            fields = line.split()
            user_id, hash_code, latitude, longitude = fields
            employee = Employee(*fields)
            # Process the data here
            print(f"Processing: {user_id}, {hash_code}, {latitude}, {longitude}")
            # Delete the row when done with processing
            file.seek(0)
            file.truncate()
            file.writelines([row for row in buffer_list if row != line])
            file.truncate()