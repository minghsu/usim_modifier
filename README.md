# USIM modifier

---
## Abstract

This is my 2nd practice project with Python, and it's a flexible SIM tool to modify some SIM files.  
Yes, the tool is not a perfect tool for USIM modify, but I think its enough for most requirement.

---
## Features

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
> - cache 1.00 > Cache the PIN1/ADM code to xml file for future verify automatically.
> - arr 1.00 > Displayed all contents of EF_ARR file.
> - gid 1.00 > Display or modify the value of GID1/GID2.
> - msisdn 1.00 > Display or modify the value of MSISDN.
> - imsi 1.00 > Display or modify the value of IMSI.
> - status 1.00 > Displayed the current status of USIM

---
## Requirement Packages

- [colorama](https://pypi.org/project/colorama/)
- [lxml](https://lxml.de/)
- [pyscard](https://pyscard.sourceforge.io/)

---
## Install "USIM modifier"

git clone https://github.com/minghsu/usim_modifier.git

---
## User Guide

If you can see simlar message with below picture, it mean the system was works fine,  
then you can type "exit" command to quit or "plugin" to get more information.  

The system will request "PIN1" (if pin1 enabled) and "ADM" verify,  
we can skip the "ADM" key verify operation, but some USIM files will not updatable.
    
![Start up](/docs/images/startup.png "Start up")

After executed "plugin" command, will list all supported plugin name, version and summary.

![Plugins](/docs/images/plugin.png "Plugins")

We use "imsi" plugin as an example, you can use "help" parameter to find help info for each plugin.
>> - imsi help: Displayed the help message of "imsi" plugin
>> - imsi: Displayed the current "IMSI"
>> - imsi format=raw: Show the raw data of "IMSI"
>> - imsi set=46692: Update the IMSI value to "46692XXXXXXXXXX"

![IMSI](/docs/images/imsi.png "IMSI")

If we skipped the "ADM" verify operation, some USIM file will not update due to the security concern.  
For more detail, please refer "ETSI TS 131 102" specification.

![ERROR](/docs/images/update_fail.png "ERROR")

---
## Tech Note

Below image is the simple diagram of USIM modifier V2 project, my goal is using "MVC" pattern but looks it still have many problem (><).

![Simple Diagram](/docs/images/simple-diagram.png "Simple Diagram")


The other parts will be coming soon ...

---
## Reference
- ETSI TS 102 221 - Smart Cards; UICC-Terminal interface; Physical and logical characteristics
- ETSI TS 131 102 - UMTS; LTE;Characteristics of the Universal Subscriber Identity Module (USIM) application
