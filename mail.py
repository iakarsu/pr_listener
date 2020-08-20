import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class MailClient():
    username = ''
    password = ''

    server = smtplib.SMTP_SSL('smtp.yandex.com', 465)

    def __init__(self, username, password, ):
        self.username = username
        self.password = password

        server = smtplib.SMTP_SSL('smtp.yandex.com', 465)
        server.ehlo()

    def sendMail(self, receiver, subject, link, date):
        self.server.login(self.username, self.password)
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

                <p>Huobi tarafından son yayınlanan makalenin adresi:
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
        self.server.sendmail(self.username, receiver, msg.as_string())




