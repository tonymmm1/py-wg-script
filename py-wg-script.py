#!/usr/bin/env python3

import os
import subprocess
import ipaddress

print ("This is a program for setting up a wireguard server and clients")

wg_server           = input("Input wireguard server interface: \t")
wg_server_hostname  = input("Input server hostname or public ip: \t")
wg_server_ip        = ipaddress.ip_address(input("Input wireguard server ip: \t\t"))
wg_server_mask      = input("Input wireguard server mask (24): \t")
wg_server_port      = input("Input wireguard server port: \t\t")

while True:
    try:
        wg_clients = int(input("Input number of clients to create: \t"))
        break
    except ValueError:
        print ("\nInput was not valid")
        continue
wg_client_dns   = input("Input dns server to use\t\t\t")
wg_allowedips   = input("Input allowed ips/mask: \t\t") 
wg_keepalive    = input("Input keepalive duration: \t\t")

def wg_server_creation():
    global wg_server
    global wg_server_ip
    global wg_server_mask
    global wg_server_port
    global wg_clients
    global wg_server_hostname
    global wg_client_dns
    global wg_keepalive

    os.mkdir(wg_server)
    os.chdir(wg_server)
    os.umask(0o077)
    wg_server_filename = wg_server + ".conf"
    wg_server_file = open(wg_server_filename,"a")
    wg_server_file.write("[Interface]")
    wg_server_file.write("\nAddress = " + str(wg_server_ip) + '/' + wg_server_mask + "\n")
    wg_server_private_gen   = subprocess.run("wg genkey > " + wg_server + "_priv" ,shell=True,capture_output=True)
    wg_server_public_gen    = subprocess.run("wg pubkey < " + wg_server + "_priv" + " > " + wg_server + "_pub",shell=True,capture_output=True)
    wg_server_private_file  = open(wg_server + "_priv","r")
    wg_server_private       = wg_server_private_file.read().strip()
    wg_server_public_file   = open(wg_server + "_pub","r")
    wg_server_public        = wg_server_public_file.read().strip()

    wg_server_file.write("PrivateKey = " + wg_server_private + "\n")
    wg_server_file.write("ListenPort = " + wg_server_port + "\n")

    for client in range(wg_clients):
        wg_server_ip = wg_server_ip + 1 #Server ip increment per client = client ip
        #wg server conf
        wg_server_file.write("[Peer]" + "\n")

        wg_client_private_gen       = subprocess.run("wg genkey > " + wg_server + "_client" + str(client) + "_priv" ,shell=True)                                             #Client Private Key
        wg_client_public_gen        = subprocess.run("wg pubkey < " + wg_server + "client" + str(client) + "_priv" + " > " + wg_server + "client" + str(client) + "_pub",shell=True)    #Client Public Key
        wg_server_preshared_gen     = subprocess.run("wg genpsk > " + wg_server + "_psk" ,shell=True)                                                           #Preshared Key 
        wg_client_private_file      = open(wg_server + "client" + str(client) + "_priv","r") 
        wg_client_private           = wg_client_private_file.read().strip()
        wg_client_public_file       = open(wg_server + "client" + str(client) + "_pub","r")
        wg_client_public            = wg_client_public_file.read().strip()
        wg_server_preshared_file    = open(wg_server + "_psk","r")
        wg_server_preshared         = wg_server_preshared_file.read().strip()

        wg_server_file.write("PublicKey = " + wg_client_public + "\n")
        wg_server_file.write("PresharedKey = " + wg_server_preshared + "\n")


        wg_server_file.write("AllowedIPs = " + str(ipaddress.ip_network(wg_server_ip)) + "\n")

        #wg client conf
        wg_client_filename = ("client" + str(client) + ".conf")
        wg_client_file = open(wg_client_filename,"a")
        wg_client_file.write("[Interface]")
        wg_client_file.write("\nAddress = " + str(ipaddress.ip_network(wg_server_ip)) + "\n")
        wg_client_file.write("PrivateKey = " + wg_client_private + "\n")
        wg_client_file.write("DNS = " + wg_client_dns + "\n")
        
        wg_client_file.write("[Peer]\n")
        wg_client_file.write("PublicKey = " + wg_server_public + "\n")
        wg_client_file.write("PresharedKey = " + wg_server_preshared + "\n")
        wg_client_file.write("AllowedIPs = " + wg_allowedips + "\n") 
        wg_client_file.write("Endpoint = " + wg_server_hostname + ":" + wg_server_port + "\n")
        wg_client_file.write("PersistentKeepalive = " + str(wg_keepalive) + "\n")

        os.remove(wg_server + "client" + str(client) + "_priv")
        os.remove(wg_server + "client" + str(client) + "_pub")
        os.remove(wg_server + "_psk")

wg_server_creation()
