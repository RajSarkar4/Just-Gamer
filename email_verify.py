import smtplib
import random
import os

class Email:
    # Initailze Attributes
    def __init__(self):
        self.email = os.environ.get("MAIL")
        self.password = os.environ.get("PASSWORD") 
        self.otp = int
        self.status = False
        self.smp = smtplib.SMTP("smtp.gmail.com", 587)
        self.smp.starttls()
        self.smp.login(self.email, self.password)

    # Generate OTP

    def generate(self):
        self.otp = random.randint(000000, 999999)
    

    # Send OTP to user mail
    def send_mail(self, user_mail):

        self.smp.sendmail(from_addr=self.email,
                    to_addrs=user_mail,
                    msg=f"Subject:Test Mail\n\nYour otp is {self.otp}")
        
    
    #Check OTP
    def check_mail(self, user_mail, user_i, otp):
        self.send_mail(user_mail)
        if user_i == otp:
            return True
        else:
            return False
    
    # Send Notification the the user
    def notify(self, user_mail):
        self.smp.sendmail(from_addr=self.email,
                          to_addrs=user_mail,
                          msg="Subject:Contest Reminder\n\nYou have joined the brawl star contest and you're match will be provided on our discord serve. Please check the match details and join accordingly and be ready before 10 minute on our server.\n\nJoin the discord server using the link below: \nhttps://discord.gg/queWZZhMRk")
            
