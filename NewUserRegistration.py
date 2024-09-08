from email.mime.text import MIMEText 
from email.mime.image import MIMEImage 
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart 
import datetime
import smtplib
import os
import string
import random
import csv



class User: 
    gmail_user = 'dev1237@gmail.com'
    gmail_password = '6FVaVDU7FLT_jGP'
    existingPassword = set()
    user_id = set()
    user_idForSearch = set()
    msg = MIMEMultipart() 
    COLUMNS = ["user_id","hash","password","name","email","Registration_dateAndTime"]
    @classmethod
    def prepareBody(cls,user_id, password):
        cls.msg = MIMEMultipart() 
        subject = "@noreply User-ID and Password"
        text = "User- id : " + cls.user_idGenerator + "\n" + "Password : " + cls.passwordGenerator() + "\nPlease use the above details to sign in to your new account."
        cls.msg['Subject'] = subject 
        cls.msg.attach(MIMEText(text))
    
    @classmethod
    def passwordGenerator(cls, length = 7):
        all_characters = string.ascii_letters + string.digits + string.punctuation[:4]
        password = ''.join(random.choice(all_characters) for i in range(length))
        try:
            with open('UserCredentials.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    cls.existingPassword.add(row[3])  # Target the 4th column (index 3)
        except FileNotFoundError:
            cls.passwordGenerator()
        if password not in cls.existingPassword:
            return password
        else:
            cls.passwordGenerator()
    
    @classmethod
    def user_idGenerator(cls):
        cls.user_id = set()
        try:
            with open('UserCredentials.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    cls.user_id.add(row[0])  # Target the 0th column
        except FileNotFoundError:
            pass

        while True:
            random_number = random.randint(10000, 99999)  # Generate a random 5-digit number
            if random_number not in cls.user_id:
                return random_number

    def recieveRequestToGenerate():
        pass
    
    @classmethod
    def addEntry(cls, nameOfTheUser, email):
        # Sending mail using api

        # Updating the entry in database now
        user_id = cls.user_idGenerator()
        password = cls.passwordGenerator()
        new_entry = { 
            "user_id" : user_id,
            "hash" : None,
            "password" : password,
            "name" : nameOfTheUser,
            "email" : email,
            "Registration_dateAndTime" : datetime.datetime.today()
        }

        with open('UserCredentials.csv',"a",newline="\n") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)

        print("Entry Added Successfully")
        return (user_id,password)
    
    @classmethod
    def addHashCode(cls,user_id, hashCode):
        with open('UserCredentials.csv', 'r') as file:
                reader = csv.reader(file)
                data = list(reader)

        # Finding the correct user_id
        for row in data[1:]:
            if int(row[0]) == int(user_id):
                row[1] = hashCode
                break
        
        # Writing the data back
        with open('UserCredentials.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    @classmethod
    def getName(cls, user_id):
        with open('UserCredentials.csv', 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Finding the correct user_id
        column_index = data[0].index("user_id")
        for row in data[1:]:
            if int(row[0]) == int(user_id):
                return row[3]
    @classmethod            
    def isUserPresent(cls, user_id)->bool:
        with open('UserCredentials.csv', 'r') as file:
                reader = csv.reader(file)
                data = list(reader)

        # Finding the correct user_id
        for row in data[1:]:
            try:
                if int(row[0]) == int(user_id):
                    return True
            except ValueError:
                pass
        return False

def requestNew(name,mail_id):
    User.sendMail(nameOfTheUser=name,email=mail_id)
