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
## Todo
- Security attribute (1st priority)

---
## User Guide

Coming soon ...

---
## Tech Note

Coming soon ...

---
## Reference
- ETSI TS 102 221 - Smart Cards; UICC-Terminal interface; Physical and logical characteristics
- ETSI TS 131 102 - UMTS; LTE;Characteristics of the Universal Subscriber Identity Module (USIM) application
