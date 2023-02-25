import poplib
from email import parser
import time
import email
import os
import time
import subprocess
run = True

# Deleting email
def delete_email():
    try:
        print("Deleting email...")
        # Deleting all emails in inbox
        for i in range(pop_conn.stat()[0], 0, -1):
            pop_conn.dele(i)
            
        pop_conn.quit()
        print("Succesfully deleted email")
        
    except Exception as e:
        print(e)

# Getting attachment from email (image)
def get_attachment():   
    try:
        print("Getting attachment")
        # Getting attachment
        data = (messages[-1]).get_payload()
        
        # Going through full payload
        for part in data:
            # If part of payload is png or jpg, downloading
            if part.get_content_type() == "image/png" or part.get_content_type() == "image/jpg":  
                # New image file
                f = open("toPrint.png","xb")
                print("Writing image data...")
                
                # Writing attachment to new file
                f.write(part.get_payload(decode=True))
                f.close
                print("Done writing!")
                
                # Deleting email when done
                delete_email()
                break  
                
    # No image in email
    except:
        print("Please supply image")
        
if True:
    # Current amount of emails
    cur_count = 0
    
    # Last amount of emails
    last_count = 0
    
    # If it has counted emamils or not, used so the first time it counts, it doesnt think there are new emails
    has_run = False
    
    while run:
        print("Establishing connection...")
        success = False
        while (not success):
            try:
                # Initializing poplib connection
                pop_conn = poplib.POP3_SSL('pop.gmail.com')
                pop_conn.user('etch.printer.2.0@gmail.com')
                pop_conn.pass_('Castle41')
                print("Connection successful")
                success = True
                
            except:
                print("Error establishing connection")
                
        success = False
        print("Getting mail...")

        # Trying to connect until it goes thru
        while (not success):
            try:
                # Retrieving messages
                messages = [pop_conn.retr(j) for j in range(1, len(pop_conn.list()[1]) + 1)]
                messages = ["\n".join(m.decode() for m in msg[1]) for msg in messages]
                messages = [parser.Parser().parsestr(msg) for msg in messages]
                print("Mail retrieval succesful")
                success = True
                
            except Exception as e:
                print(e)
        # Resetting counter
        cur_count = 0
        
        # Counting total messages
        for message in messages:
            cur_count += 1

        print("There are " + str(cur_count) + " emails in the inbox")
            
        # Checking if there is a new email (count is greater than last time)
        if (last_count < cur_count):
            # Making sure it isn't first count
            if (has_run): 
                print("New email recieved!")
                get_attachment()
 
        # Updating
        has_run = True
        last_count = cur_count
