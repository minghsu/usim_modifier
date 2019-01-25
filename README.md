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
- Already support below plugins:
> - iccid 1.00 > Display or modify the value of ICCID.
> - spn 1.00 > Display or modify the value of SPN.
> - dir 1.00 > Displayed all contents of EF_DIR file.
> - send 1.00 > Send the APDU command to USIM directly
> - mccmnc 1.00 > Display or modify the value of MCC/MNC.
> - atr 1.00 > Displayed the value of Answer To Reset (ATR).
> - pin_cache 1.00 > Cache the PIN1/ADM code to xml file for future verify automatically.
> - arr 1.00 > Displayed all contents of EF_ARR file.
> - gid 1.00 > Display or modify the value of GID1/GID2.
> - msisdn 1.00 > Display or modify the value of MSISDN.
> - imsi 1.00 > Display or modify the value of IMSI.
> - card_info 1.00 > Displayed the current status of USIM

---
# Requirement Packages

- [colorama](https://pypi.org/project/colorama/)
- [pyscard](https://pyscard.sourceforge.io/)  
- [lxml](https://lxml.de/)  

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
> mac@osx:/$ brew install swig.  (PS. install “swig” by homebrew)
> mac@osx:/$ pip3 install pyscard  

---
# Install "USIM modifier"

git clone https://github.com/minghsu/usim_modifier.git

---
# User Guide

Please refer [USIM Modifier User Guide](https://github.com/minghsu/usim_modifier/blob/master/docs/usim_modifier_user_guide.pdf) 

---
# Tech Note

Please refer [USIM Modifier Tech_Note](https://github.com/minghsu/usim_modifier/blob/master/docs/usim_modifier_tech_note.pdf)

---
# Reference
- ETSI TS 102 221 - Smart Cards; UICC-Terminal interface; Physical and logical characteristics
- ETSI TS 131 102 - UMTS; LTE;Characteristics of the Universal Subscriber Identity Module (USIM) application
