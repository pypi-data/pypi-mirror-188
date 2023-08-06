# Py IP Checker

With **Py IP Checker** you can get IP info.

## Installation

``bash
pip install Py-IP-Checker``

## Examples

``python
>>> from Py-IP-Checker import IP
>>> 
>>> data = IP('88.88.88.88')
>>> data.country
'Norway'
>>> data.IPtype
'IPv4'
>>> data.connection_org
'Telenor Norge AS'``

## Variables

IP
IPtype
continent
continent_code
country
country_code
region
region_code
city
lat
lon
postal
calling_code
capital
borders
emoji
emoji_unicode
connection_asn
connection_org
connection_isp
connection_domain
timezone_id
timezone_abbr
timezone_offset
timezone_utc
current_time