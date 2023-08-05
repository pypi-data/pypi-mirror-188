# Python HdbReader

HDB++ is the Tango Control System Archiving Service.
This python3 module provides extraction from multiple hdb++ engines using AbstractReader class API.
For legacy archiving and full hdb++ api (MySQL only) use PyTangoArchiving instead.

www.tango-controls.org
https://gitlab.com/tango-controls/hdbpp

Other related projects providing similar functionality, but not AbstractReader class implementation:

 - https://gitlab.com/tango-controls/hdbpp/pytangoarchiving : provides legacy and HDB++ extraction and configuratio api's (python 2 only)

 - https://github.com/dvjdjvu/hdbpp : python 3 API for extraction/configuration of MySQL/PostgreSQL HDB++ databases, by djvu@inbox.ru


## Install

Just use pip3 :
```
pip3 install pyhdbpp
```

To install run from the project directory :
```
python3 -m pip install .

```
