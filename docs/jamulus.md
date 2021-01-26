
### References
* https://jamulus.io/wiki/Installation-for-Linux#install-dependencies
* https://jamulus.io/wiki/Choosing-a-Server-Type
* https://jamulus.io/wiki/Server-Linux#running-a-headless-server


### Headless server installation

1. Download the source
   https://github.com/corrados/jamulus/archive/latest.tar.gz
   
2. Install dependencies
   First, update your package list (e.g. on Debian based distributions with sudo apt-get update).

   On Ubuntu-based distributions 18.04+, Debian 9+ or 10 and Raspberry Pi Raspbian Buster release or later:
   ```shell
   sudo apt-get install build-essential qt5-qmake qtdeclarative5-dev qt5-default qttools5-dev-tools libjack-jackd2-dev 
   ```
   
   On Fedora:
   ```shell
   sudo dnf install qt5-qtdeclarative-devel jack-audio-connection-kit-dbus jack-audio-connection-kit-devel
   sudo dnf install qt-devel
   ```
   
   Qjackctl: Optional, but recommended

   QjackCtl is a utility to help you set up the Jack audio server (installed as part of the dependencies above). Install it via e.g.
   ```shell
   $ sudo apt-get install qjackctl
   ```
   
   You may also wish to consider using a low-latency kernel (eg. for Ubuntu 18.04: sudo apt-get install linux-lowlatency-hwe-18.04).

3. Compile Jamulus

   Now cd into the jamulus sources directory you downloaded:
   ```shell
   $ cd jamulus-latest
   ```

   Now compile the sources with the following commands (the last make may take several minutes to run):
   ```shell
   $ qmake-qt5 Jamulus.pro
   $ make clean
   $ make
   $ make install
   ```

4. Configure firewall
   
   By default, Jamulus listens on port 22124 on all interfaces.
   You'll need to add a rule to allow traffic on the Jamulus port.
   
   Typically, you would want to allow access to the Jamulus server only from a specific IP address or IP range, 
   For example, to allow connections only from the 192.168.2.0/24 range, enter the following command:
   
   ```shell
   $ sudo firewall-cmd --new-zone=jamulus --permanent
   $ sudo firewall-cmd --zone=jamulus --add-port=22124/udp --permanent
   $ sudo firewall-cmd --zone=jamulus --add-source=192.168.2.0/24 --permanent
   $ sudo firewall-cmd --reload
   ```
5. Configure port forwarding
   In your internet router, configure port forwarding.
   No details are provided because it differs per router. This section serves only as a reminder.
   
6. Headless 
   Create a user called jamulus.
   A home folder is created, because this will hold html status of the server.
   ```shell
   $ adduser jamulus
   ```
   
   #### Create the start script jamulus.service
   
   ```shell
   [Unit]
   Description=Jamulus-Server
   After=network.target

   [Service]
   Type=simple
   User=jamulus
   Group=users
   Nice=-20
   IOSchedulingClass=realtime
   IOSchedulingPriority=0

   ExecStart=/usr/local/bin/Jamulus -s -n -t -m "/home/jamulus/snapsnare" -R "/home/jamulus/recordings"

   Restart=on-failure
   RestartSec=30
   StandardOutput=journal
   StandardError=inherit
   SyslogIdentifier=jamulus

   [Install]
   WantedBy=multi-user.target
   ```
   
   copy the startup script jamulus.service to /etc/systemd/system:
   ```shell
   $ sudo cp jamulus.service /etc/systemd/system/jamulus.service
   $ chmod 644 /etc/systemd/system/jamulus.service
   ```
 
   start jamulus.service:
   ```shell
   $ sudo systemctl start jamulus.service
   ```

   status jamulus.service:
   ```shell
   jamulus.service - Jamulus-Server
     Loaded: loaded (/etc/systemd/system/jamulus.service; enabled; vendor preset: disabled)
     Active: active (running) since Mon 2021-01-25 14:54:49 CET; 21s ago
   Main PID: 515434 (Jamulus)
      Tasks: 3 (limit: 16686)
     Memory: 40.5M
        CPU: 37ms
     CGroup: /system.slice/jamulus.service
             └─515434 /usr/local/bin/Jamulus -s -n -t -m /home/jamulus/snapsnare -R /home/jamulus/recordings

   Jan 25 14:54:49 192.168.2.123 systemd[1]: Started Jamulus-Server.
   Jan 25 14:54:49 192.168.2.123 jamulus[515434]: - server mode chosen
   Jan 25 14:54:49 192.168.2.123 jamulus[515434]: - no GUI mode chosen
   Jan 25 14:54:49 192.168.2.123 jamulus[515434]: - translations disabled
   Jan 25 14:54:49 192.168.2.123 jamulus[515434]: - HTML status file name: /home/jamulus/snapsnare
   Jan 25 14:54:49 192.168.2.123 jamulus[515434]: - recording directory name: /home/jamulus/recordings
   Jan 25 14:54:49 192.168.2.123 Jamulus[515434]: Recording state enabled
   Jan 25 14:54:49 192.168.2.123 jamulus[515434]:  *** Jamulus, Version 3.6.2
   Jan 25 14:54:49 192.168.2.123 jamulus[515434]:  *** Internet Jam Session Software
   Jan 25 14:54:49 192.168.2.123 jamulus[515434]:  *** Released under the GNU General Public License (GPL)
   ```
   
   enable jamulus.service:
   start jamulus during boot.
   
   ```shell
   $ sudo systemctl enable jamulus.service
   
   Created symlink /etc/systemd/system/multi-user.target.wants/jamulus.service → /etc/systemd/system/jamulus.service
   ```
