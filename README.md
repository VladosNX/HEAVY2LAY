# HEAVY2LAY
*Really HEAVY DOS for careful goals
V1.0 - developed by [vladosnx](https://github.com/vladosnx) on github*

## DISCLAIMER
This program wasn't developed to hack real sites. Use it only for pentesting. Only YOU're responsible for your actions.

## About and what's this
HEAVY2LAY - simple program calls hard **Denial-of-Service** to test your service.
Written on Python 3, uses unlimited sockets amount to send them to your target and call overload on site server.

## Usage
Before you start please make sure you have a *Python 3* installed on your system. If it isn't, you can find it on the [official Python site](https://python.org).
After Python 3 is installed, open the command line at the program folder.
General usage:
> heavy2lay.py  -h [host] -p [port] -s [sockets] -S [sleeptime]
#### Explanation
**host** *(required)*- specifies target host name
**port** *(default is 80 for http and 443 for https)*- specifies target port
**sockets** *(default is 100)*- amount of socket to seng to target at the same time
**sleeptime** *(default is 15)* - sleep time between loops *(in seconds)*

---
*By [VladosNX](https://github.com/vladosnx)*
