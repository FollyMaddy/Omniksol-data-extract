# Omniksol-data-extract
Extract data from access point website of older Omniksol with wifi module.

--------------------------------------------------------------------------

In 2021 I got my hands on a free Omniksol-4k-tl PV inverter with wifi module which had a defect.

After research it seemed that a common failure is that 1 or more relais will fail.

Mine had one defective relais and had it repaired and it's still working in 2026.

Another issue with the Omniksol is that the solarpanels have to be strong enough.

Earlier connected panels, connecting 6, providing less than 125 Wp per panel made the inverter give an error : Isolation Fail .

Now connecting 6 panels providing 275 Wp per panel make the inverter work as expected.

--------------------------------------------------------------------------

I have a wifi module on board.

It has it's own SIDD with protected password.

If you don't know the password then you need to reset the wifi setting.

In the menu of the inverter you have to press until you find the IP adres then hold the button until you see : NO .

Now you can release the button and by pressing shortly you can select : YES .

Holding the button again will save the setting and the wifi settings will be the default without password.

Now you can connect to the inverter with wifi.

Go to your browser and insert 10.10.100.254 as adress.

It will ask you for a username/password.

The default is : admin/admin .

Now you can alter the passwords to your needs.

Go to "Advanced" and select "accesspoint" if you want to use original inverter SIDD.

There you can change the password for the SIDD.

--------------------------------------------------------------------------
Next issue :

Turns out the producer of the product no longer exists and the remote servers seem to be down too.

However, on github there are some repositories to intercept the data or push the data to a remote server.

For me, these projects seem to be too difficult and overcomplicated.

So I made a simple bash line, using curl, to extract the data from access point website.

Cutting out the data can also be done with micropython so we can also use a Raspberry Pi Pico1w or Pico2w.

I have used these methodes for other projects, however, with the Omniksol I stumbled upon 2 problems.

When accessing the webpage of the Omniksol you need a username and a password to get access which makes it difficult to get the data.

Further investigation revealed that it uses javascript "pages" that contain the data.

I found that accessing the javascript-page is possible without using the username and password :

```
curl http://10.10.100.254/js/status.js
```

Now we can cut out some CSV data, containing the model and a few PV statistics, like this :

```
curl http://10.10.100.254/js/status.js|cut -d '"' -f16
```

After that, it's possible to automate this and display and add the CSV data of every 5 minutes :

(curl -s is used to run curl into silence mode)

```
while true;do curl -s http://10.10.100.254/js/status.js|cut -d '"' -f16|while read line;do echo $(date|sed 's/ /,/g'),$line;done;sleep 300;done
```

A bit more sophisticated to extact the CSV data to variables to recreate the CSV with only the data I wanted :

```
while true;do curl -s http://10.10.100.254/js/status.js|cut -d '"' -f16|while read line;do echo $(date|sed 's/ /,/g'),$line|while IFS="," read -r c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17;do echo $c1,$c2,$c3,$c4,$c5,$c6,$c13,$c14\0;done;done;sleep 300;done
```

Now we can choose from the last 2 bash lines to extract the basic PV data from the Omniksol.

Just paste the text into an empty text.csv file and you can open it with, for example, libreoffice calc to create a chart.

Now that we can extract the data it's also possible to switch a led or a relay when the "current power" is above a certain value making a GPIO of a Raspberry high or low using pinctrl :

(remember, change to your needs : op = configure pin as output / pn = not enable pull resistor / dl = driving low / dh = driving high / switch when the power is greater than 500 W)
```
while true;do power=$(curl -s http://10.10.100.254/js/status.js|cut -d '"' -f16|cut -d, -f 6);echo $power;if [[ $power -gt 500 ]];then echo on;pinctrl set 2 op pn dl;else echo off;pinctrl set 2 op pn dh;fi;sleep 300;done
```

--------------------------------------------------------------------------

I have added a micropython program for the PICO1W/PICO2W which can do somewhat the same.

The program might work on other microcontrollers too.

Nice thing about these microcontrollers is that they use far less power than RPI's or other computers.

Please search the internet on how to user micropython on your microcontroller and then add the program via Thonny, for example.

Remeber, if you want to run the program without Thonny and just on the microcontroller then rename the program as main.py and copy it to your PICO with Thonny.

The program has been added as omniksol.py.

(remember to add your SIDD and PASSWORD in the program)

--------------------------------------------------------------------------

I hope this information it's usefull to someone.

Happy extracting !
