In order to send emails through gmail the python smtplib library is used.
Our own email is used, for this you have to setup your google account, to allow less secure apps.
A switch is shown, turn it on.
https://myaccount.google.com/lesssecureapps

A better option is using google cloud.
This requires more configuration though:
- create a project and enabling the gmail api
- create a service account that has access to your gmail account

References:
  - https://developers.google.com/gmail/api/quickstart/python
  - https://mailtrap.io/blog/send-emails-with-gmail-api/  
  - https://developers.google.com/gmail/api/reference/rest?apix=true
  
