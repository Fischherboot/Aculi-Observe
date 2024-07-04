![download.png](https://raw.githubusercontent.com/Fischherboot/Aculi/main/watermark-no-bg.png)

# Aculi Observe

This is a programm for my homelab, but you can use it if you want!
It uses a ``host.py`` and a ``client.py`` to update system information.

### How to use

execute the pip install commands from the ``requirements-lol.txt``

then, go to your host machine, it can be a full server or even a raspberry pi.
just start the host.py on there, write down its ip adress and open port 5000 in the local network so that the client can reach it.

only after the host has been setup, go to a client machine.
then start the client.py
it will ask you for two pieces of information.

Enter the local IP of the host server: ``*enter the ip of the host*``

Enter a name for this client: ``*enter a name for the client, it will be displayed on the host*``

then it'll update the sys info every 15 seconds, sending it to the host.

### Current problem:

Host website doesnt update automatically, have to relaod it to see current information.

bad looking web-gui

hard to use for non tech ppl
