# expired-cert-calendar
This tool generates a calendar of expired certificates in an IBM Security Access Manager (ISAM) appliance. 

## Requirements
* requests
* ics
* ibmsecurity

```python
pip install -r requirements.txt
```

## Usage
In expired_certs.py:
* set the hostname, username and password of the ISAM appliance
* set the reminder in the Calendar events (default is 14 days)

```python
$ python expired_certs.py
```

