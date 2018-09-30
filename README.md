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
> - atr: Displayed the value of Answer To Reset (ATR).
> - cache: Cache the PIN1/ADM code to xml file for future verify automatically.
> - dir: Displayed all contents of EF_DIR file.
> - gid1: Display or modify the value of GID1.
> - iccid: Display or modify the value of ICCID.
> - imsi: Display or modify the value of IMSI.
> - mccmnc: Display or modify the value of MCC/MNC.
> - msisdn: Display or modify the value of MSISDN.
> - send: Send the APDU command to USIM directly
> - spn: Display or modify the value of SPN.
> - status: Displayed ICCID, IMSI, MCC/MNC, SPN & GID1 values of USIM.

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

Coming soon ...

---
## Tech Note

Coming soon ...
