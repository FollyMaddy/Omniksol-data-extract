# Omniksol-data-extract
Extract data from access point website of older Omniksol with wifi module.

--------------------------------------------------------------------------

Recently I got my hands on a free Omniksol-4k-tl PV inverter with wifi module which had a defect.

After research it seemed that a common failure is that 1 or more relais will fail.

Mine had one defective relais and had it repaired.

Another issue with the Omniksol is that the solarpanels have to be strong enough.

Earlier connected panels, connecting 6, providing less than 125 Wp per panel made the inverter give an error : Isolation Fail .

Now connecting 6 panels providing 275 Wp per panel make the inverter work as expected.

--------------------------------------------------------------------------

I have a wifi module on board.

If it has it's own SIDD with protected password.

If you don't know the password then you need to reset the wifi setting.

In the menu of the inverter you have to press until you find the IP adres then hold the button until you see : NO .

Now you can release the button and by pressing shortly you can select : YES .

Holding the button again will save the setting and the wifi settings will be the default without password.

Now you can connect to the inverter with wifi.

Go to your browser and insert 10.10.100.254 as adress.

It will ask you for a username/password.

The default is : admin/admin .

Now you can alter the passwords to your needs.

--------------------------------------------------------------------------
Next issue :

Turns out the producer of the product no longer exists and the remote servers seem to be down too.

However, on github there are some repositories to intercept the data or push the data to a remote server.

For me, these projects seem to be too difficult.

So I made a simple bash line, using curl, to extract the data from access point website.

I have used this methode also for other devices, however, with the Omniksol I stumbled upon 2 problems.

The webpage is protected with a username and a password and, when accessed, the data isn't exposed in the text.

Further investigation revealed that it uses javascript "pages" that contain the data.

Accessing the javascript "page" is possible without using a username and a password :

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
while true;do curl -s http://10.10.100.254/js/status.js|cut -d '"' -f16|while read line;do echo $(date|sed 's/ /,/g'),$line;done;sleep 300;don
```

A bit more sophisticated to extact the CSV data to variables to recreate the CSV with only the data I wanted :

```
while true;do curl -s http://10.10.100.254/js/status.js|cut -d '"' -f16|while read line;do echo $(date|sed 's/ /,/g'),$line|while IFS="," read -r c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17;do echo $c1,$c2,$c3,$c4,$c5,$c6,$c13,$c14\0;done;done;sleep 300;done
```

Now we can choose from the last 2 bash lines to extract the basic PV data from the Omniksol.

Just paste the text into an empty text.csv file and you can open it with, for example, libreoffice calc to create a chart.

I hope this information it's usefull to someone.

Happy extracting !
