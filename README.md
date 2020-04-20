# py-wg-script
## Release: 0.1.0

This program will generate a wireguard configuration file as well as corresponding clients. 

### Requirements:
```
pip install ipaddress #Library dependency for Python3 
```

### Running:
```
chmod +x py-wg-script.py
./py-wg-script.py
cp (interface)/(interface).conf /etc/wireguard
systemctl enable wg-quick@(interface)
systemctl start wg-quick@(interface)
```
