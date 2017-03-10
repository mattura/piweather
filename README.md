# piweather
Raspberry Pi &amp; SSD1306 OLED project

This project uses a Raspberry Pi B, a Wireless USB dongle and an SSD1306 OLED display to display the current weather and train times for selected locations. Optionally, add a rotary encoder and add your own menus!
<img src="weather.jpg">

<h2>Hardware</h2>
<ul>
<li>Raspberry Pi</li>
<li>Compatible USB WiFi dongle</li>
<li>SD Card (at least 8GB)</li>
<li>Power supply</li>
<li>SSD1306 OLED Display</li>
<li>Jumper wires (7-10)</li>
<li>(optional) Rotary encoder, soldering iron, wire, solder-sucker</li>
<li>(temporarily) Screen + HDMI cable + keyboard (setup directly) OR ethernet cable + router + computer (setup via SSH)</li>
</ul>

<h2>Software</h2>
<h4>Initial setup:</h4>
<p>Prepare your Pi if possible by using a fresh installation of the <a href="https://www.raspberrypi.org/downloads/raspbian/">latest Raspbian</a>. Burn this to your SD card and connect to your Pi using one of the following methods:</p>
<p><b>A.</b> Connect up your ethernet cable between your Pi and router and log in to your Pi using SSH (<a href="http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html">Putty</a> on Windows). If you can connect using avahi/Bonjour, the address you need is <b>raspberrypi.local</b>, otherwise find the Pi's IP address by logging in to your router.<br/>
<b>NOTE</b>: You will first need to place a blank file <b>ssh</b> on the /boot/ partition in order to enable SSH!<br/> This is a new security measure in builds released since November 2016.</p>
<p><b>B.</b> Connect keyboard and monitor to your Pi.</p>

<p>The default login username is <b>pi</b> and the password is <b>raspberry</b>. You can change this in the next step or by using the <b>passwd</b> command.</p>

<p>Run <code>sudo raspi-config</code> to set up your Pi. Go through options 1-4 in turn, and it is considered safe to overclock a little (I used the Medium setting, but whatever works for you). In the Advanced options (7), enable SSH, SLI and I2C. Reboot and then update the pi: <code>sudo apt-get update && sudo apt-get upgrade</code></p>

<h4>Connect to WiFi:</h4>
<p>Plug in your WiFi dongle and check it is recognised using <code>lsusb</code>. Then check the interface appears with <code>ifconfig</code>. You should have a <b>wlan0</b> or similar but with no IP address. A good way to add a WiFi network is by using the interface <code>wpa_cli</code>. This allows a number of commands to interact with your dongle. Search for WiFi networks using the commands <code>scan</code> followed by (give it a few seconds) <code>scan_results</code>. Add a new network: <code>add_network</code> and note the number returned (the first time this will be 0, if not, change in the following commands). Use the commands <code>set_network 0 ssid "YOUR_SSID"</code> and <code>set_network 0 psk "YOUR_PASSWORD"</code>. Then, <code>enable_network 0</code>. You should hopefully see "Associated with...", meaning you have connected. Finally, <code>save_config</code> and <code>quit</code>. You can tinker with the config later if necessary with <code>sudo nano /etc/wpa_supplicant/wpa_supplicant.conf</code>. Finally, check the configuration survives a reboot by <code>sudo reboot</code>, unplug the ethernet cable (or disconnect monitor & keyboard), and try to ssh over WiFi to <b>raspberrypi.local</b>.
</p>

<h4>Prerequisites:</h4>
</ul>
<li>Pip: <code>wget https://bootstrap.pypa.io/get-pip.py</code>, then <code>sudo python get-pip.py</code></li>
<li>Git: <code>sudo apt-get install git</code></li>
<li>This very handy Darwin SOAP client provided by <a href="https://github.com/robert-b-clarke/nre-darwin-py">Robert Clark</a>: <code>sudo pip install nre-darwin-py</code></li>
<li>This library by Adafruit which enables drawing text and shapes on the SSD1306 OLED: <code>git clone <a href="https://github.com/adafruit/Adafruit_Python_SSD1306.git">Adafruit_Python_SSD1306</a></code>, <code>cd Adafruit_Python_SSD1306/</code>, <code>sudo python ez_setup.py install</code></li>

<li><a href="https://github.com/Gadgetoid/WiringPi2-Python.git">wiringPi2-Python</a> (follow the instructions in the link to install wiringPi)</li>
<li>sudo apt-get install python-dev</li>
<li>sudo apt-get install python-PIL</li>
<li>sudo pip install spidev</li>
</ul>
</p>

<h4>PiWeather:</h4>
<p>Then clone this repository to your pi:<br/>
<code>git clone https://github.com/mattura/piweather</code><br/>
</p>

<p>Place any True Type font you want in the /fonts/ directory and edit the code,
I used Minecraftia and Everyday (both free for personal use) from here:<br/>
http://www.dafont.com/minecraftia.font<br/>
http://www.dafont.com/everyday.font<br/>
</p>

Check your screen runs correctly:<br/>
<code>python scrtest.py</code><br/>

<p>To access the Met Office Datafeed, you need to register for an api key. Once you have this, copy the key value into the "met.conf" file.</p>
<p>To access the National Rail OpenLDBWS data feed, you need to register for a token. Once you have this, place it into the "nre.conf" file.</p>
<p>Check your apikey and token work:<br/>
Run <code>python cron.py</code> and check for errors, then run <code>ls *.dat</code> and check the dat files have been created</p>
<p>Set up your crontab to run cron.py at regular intervals. I run it every minute between the hours of 5am and 11pm:<br/>
<code>sudo crontab -e</code><br/>
<code>* 5-23 * * * /usr/bin/python /home/pi/piweather/cron.py</code>
</p>
<p>Now you should be set! Try <code>python display.py</code><br/>
If it works, you can run it on boot by adding a script in <code>/etc/rc.local</code>
</p>
