import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import ssl


class MailClient():
    username = ''
    password = ''


    def __init__(self, username, password, ):
        self.username = username
        self.password = password


    def sendMail(self, receiver, subject, link, date):
        image_address = 'https://pbs.twimg.com/profile_images/1236606882913161216/jPqB3_dD_400x400.jpg'
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = receiver
        msg['Subject'] = '[ Huobi New PR ] ' + subject


        html ="""\
            <html>
            <head></head>
            <body style="text-align:center;">
                <div>
                <p> Merhaba! </p>


                <p>Huobi ile ilgili PRNewsWire tarafından son yayınlanan makalenin adresi:
                    <a href={link}> bağlantı </a>
                </p>


                <p>Yayınlanma tarihi: {date}</p>
                </div>
                <div>
                    <img src={image}>    
                </div>
            </body>
            </html>
            """.format(link=link, date=date, image=image_address)
    
        part1 = MIMEText(html, 'html')
        msg.attach(part1)  
        try: 
            context = ssl.create_default_context()
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.ehlo()  
                server.starttls(context=context)
                server.ehlo() 
                server.login(self.username, self.password)
                server.set_debuglevel(1)
                server.sendmail(self.username, receiver, msg.as_string())
            print('mail has been sendedd')
        except smtplib.SMTPRecipientsRefused as e:
            print("mail couldn't send")
            message = e.args[0]['no-such-receiver@comcast.com'][1]
            print(message)