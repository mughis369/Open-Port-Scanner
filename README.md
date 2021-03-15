# Open-Port-Scanner
This script scans for open ports of a given address. You can also define port range to scan.

Usage
-----------

Using the command script would scan target-ip for open ports in the range of 1-1000.
```
python port_scanner.py target_ip 1 1000
```


***Use Case I***

In this example google.com is target and 70 is starting port and 90 is last port to be scanned, script would scan google.com for open ports in the range of 70-90
```
python port_scanner.py google.com 70 90
```
 


***Use Case II***

if port range is not mentioned script will simply scan for all ports

```
python port_scanner.py google.com
```

**To chech accuracy of the script you can perform a small range scan like 1-1000 it will give you results fast and you can compare those with nmap.**

----------------------------------------------------------------------------
