import os
import sys
import time

def slowPrint(s):
  for c in s :
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(0.01)

def setup():
    print(r"""
 ___      _   _                ___ _         _   
| _ \_  _| |_| |_  ___ _ _    / __| |_  __ _| |_ 
|  _/ || |  _| ' \/ _ \ ' \  | (__| ' \/ _` |  _|
|_|  \_, |\__|_||_\___/_||_|  \___|_||_\__,_|\__|
     |__/                                        
""")
    choice_made = False
    while not choice_made:
        slowPrint("Voulez vous Héberger un salon ou en Rejoindre un ? (H / R) : ")
        choice = input().upper()
        if choice == "H":
            host()
            choice_made = True
        elif choice == "R":
            client()
            choice_made = True

def host():
   return None

def client():
   return None


setup()
input()