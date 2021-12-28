References
=
* https://fedoraproject.org/wiki/Nginx
* https://fedoraproject.org/wiki/Https#openssl
* https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04

## Python Flask-capable webhosts
https://www.pythonanywhere.com/
https://stackabuse.com/deploying-a-flask-application-to-heroku/
https://www.reddit.com/r/flask/comments/2321oc/easiest_and_fastest_way_to_host_flask_python/


## Nginx and Flask
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
https://stackoverflow.com/questions/46257171/starting-uwsgi-instance-fails-with-code-203
https://fedoraproject.org/wiki/Nginx

permission denied issue cause
https://superuser.com/questions/809527/nginx-cant-connect-to-uwsgi-socket-with-correct-permissions

in the link below is shown how audit2why works
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/security-enhanced_linux/sect-security-enhanced_linux-fixing_problems-allowing_access_audit2allow

use this command to show the error

$ audit2why -a





Installing nginx
as root

$ dnf install nginx
$ dnf install nginx-all-modules

chown -R jan:users *
usermod -aG users jan


allow execStart on your python virtual environment
chcon -R -t bin_t /home/jan/uwsgi-snapsnare-0.0.10/venv/bin/
