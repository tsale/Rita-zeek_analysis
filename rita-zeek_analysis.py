import subprocess
import os
import argparse


def args():
    global install
    global analyze
    global datasetname
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--install", help="[*] Install Rita/Zeek/MongoDB for Ubuntu 20.4",required=False, action="store_true")
    parser.add_argument("-a","--analyze", help="[*] Convert PCAPs to zeek logs and analyze with rita ",required=False, action="store_true")
    parser.add_argument("-d","--datasetname", help="[*] Dataset name of the rita import (Dataset name)")
    args = parser.parse_args()
    install = args.install
    analyze = args.analyze
    datasetname = args.datasetname

def install_all():
  #Setup Rita-Zeek-mongodb on Ubuntu 20.4

  # Download and install Rita which will also install Zeek
  rita = os.getcwd() + "/rita"
  subprocess.call("git clone https://github.com/activecm/rita.git",shell=True)
  subprocess.call(f"chmod +x {rita}/install.sh",shell=True)
  subprocess.run(f"{rita}/install.sh --disable-mongo", shell=True)

  #  # Install and configure MongoDB (you also have to install and configure docker if you haven't already)
  subprocess.call("apt-get install docker.io -y", shell=True)
  subprocess.call("apt-get install wireshark-common -y", shell=True) # Installing mergecap
  subprocess.call("docker run -d --name MongoDB mongo:4.2", shell=True)
  print("[*] You will now have 	to edit /etc/rita/config.yaml \
to add the IP of the MongoDB container. You can view the IP \
by typing: sudo docker inspect MongoDB")

def merge(dir_name):
  # Using mergecap to merge PCAPs. You should install it if you don't have it installed already.
    print(f"Selected directory: {dir_name}","\n")
    print(f"Merging all PCAPs in {dir_name} to merge.pcap...") 
    subprocess.call(f"mergecap -w merged.pcap {dir_name}/*.pcap", shell=True)

def analyze_pcaps(dbname,dir_name):
  print("\n\t[*] Converting merged PCAP to zeek logs...\n")
  subprocess.call(f"""zeek -r {dir_name}/*.pcap local "Log::default_rotation_interval = 1 day"
    """, shell=True)
  print("\t[*] Analyzing zeek logs with RITA...\n")
  subprocess.call(f"rita import {dir_name}/*.log {dbname}",shell=True)
  
  print("\t[*] Exporting RITA results to HTML report... \n")
  subprocess.call(f"rita html-report {dbname}", shell=True)
  print("\n[*] DONE!")

if __name__ == '__main__':
  args()
  if install:
    install_all()
  elif analyze:
    dir_name = input("Type the full PATH of the PCAP directory: \
(Press ENTER if they are in your current directory) ")
    if dir_name == "":
      dir_name = os.getcwd()
    read = input("[*] Do you have PCAPs to merge? (y/n) ")
    if read.lower().startswith("y"):
      merge(dir_name)
    analyze_pcaps(datasetname,dir_name)