# USIM modifier

---
# Abstract

This is my 2nd practice project with Python, and it's a flexible SIM tool to modify some SIM files.  
Yes, the tool is not a perfect tool for USIM modify, but I think its enough for most requirement.

---
# Features

- Interactive mode
- Flexible plugin mechanism
- Logging supported
- Below plugins were supported
> - iccid: Display or modify the value of ICCID.
> - spn: Display or modify the value of SPN.
> - dir: Displayed all contents of EF_DIR file.
> - send: Send the APDU command to USIM directly
> - mccmnc: Display or modify the value of MCC/MNC.
> - atr: Displayed the value of Answer To Reset (ATR).
> - pin_cache: Cache the PIN1/ADM code to xml file for future verify automatically.
> - arr: Displayed all contents of EF_ARR file.
> - gid: Display or modify the value of GID1/GID2.
> - msisdn: Display or modify the value of MSISDN.
> - imsi: Display or modify the value of IMSI.
> - card_info: Displayed the current status of USIM

---
# Card Info Example
![Card Info](https://minghsu.github.io/usim_modifier/docs/images/card_info.png)

---
# Requirement Packages

- [colorama](https://pypi.org/project/colorama/)
- [pyscard](https://pyscard.sourceforge.io/)  
- [lxml](https://lxml.de/)  

---
# Special Thanks

Brian Beck: [switch class](http://code.activestate.com/recipes/410692/)

---
# Prepare the environment

## Linux
> linux@ubuntu:/$ pip3 install colorama  
> linux@ubuntu:/$ sudo apt-get install swig  
> linux@ubuntu:/$ sudo apt-get install libpcsclite-dev  
> linux@ubuntu:/$ sudo pip3 install pyscard

## MAC OSX
> Pre-condition: “HomeBrew” must be installed.  
  
> mac@osx:/$ pip3 install colorama  
> mac@osx:/$ pip3 install lxml  
> mac@osx:/$ brew install swig  (PS. install “swig” by homebrew)  
> mac@osx:/$ pip3 install pyscard  

---
# Install "USIM modifier"

git clone https://github.com/minghsu/usim_modifier.git

---
# User Guide

Please refer [USIM Modifier User Guide](https://github.com/minghsu/usim_modifier/blob/master/docs/usim_modifier_user_guide.pdf) 

---
# Tech Note

Please refer [USIM Modifier Tech Note](https://github.com/minghsu/usim_modifier/blob/master/docs/usim_modifier_tech_note.pdf)

---
# Reference
- ETSI TS 102 221 - Smart Cards; UICC-Terminal interface; Physical and logical characteristics
- ETSI TS 131 102 - UMTS; LTE;Characteristics of the Universal Subscriber Identity Module (USIM) application
