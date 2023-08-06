# python-wmi-client-wrapper (forked for Python3 support)

This repo contains a fork from [python-wmi-client-wrapper](https://github.com/kanzure/python-wmi-client-wrapper)
by [kanzure](https://github.com/kanzure); the changes are roughly as follows:

- Add Python3 support
    - Naive approach, just using [future](https://pypi.org/project/future/) to do the hard work (boilerplate at top of each file for
      compatibility layer)
- Add support for `domain` parameter in `WmiClientWrapper` constructor
    - Thanks to [ArminNaCl](https://github.com/ArminNaCl) for the contribution!
- Bump version of [future](https://pypi.org/project/future/) to handle [CVE-2022-40899](https://github.com/advisories/GHSA-v3c5-jqr6-7qm8)
    - Thanks to [yotamc-ms](https://github.com/yotamc-ms) for the contribution!

To install this forked version:

```
pip install wmi-client-wrapper-py3
```

The rest of this README is verbatim of the original repo.

---

This is a wrapper around wmi-client for Linux. Apparently the python-wmi module
uses Windows APIs to access WMI, which isn't something that is going to work on
Linux.

## installing

```
pip install wmi-client-wrapper
```

## usage

```
import wmi_client_wrapper as wmi

wmic = wmi.WmiClientWrapper(
    username="Administrator",
    password="password",
    host="192.168.1.149",
)

output = wmic.query("SELECT * FROM Win32_Processor")

#get FibrePort Info
wmic = wmi.WmiClientWrapper(
    username="Administrator",
    password="password",
    host="192.168.1.1",
    namespace='//./root/WMI'
)
output = wmic.query('Select * FROM MSFC_FibrePortNPIVAttributes')

```

## testing

```
nosetests
```

## license

BSD
