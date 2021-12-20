G-CAT ID Manager
==================
# Intoroduction
G-CAT ID Manager is a tool that stores readable IDs (like ID00001) and UUIDs (like aaaaaaaa-1111-4bbb-r222-cccccccccccc) in MySQL database, and support conversion.
It is designed for cancer genome analysis, but can be used for any system that needs to convert between readble IDs and UUIDs.

# Installation
## Install MySQL server
G-CAT ID Manager requires MySQL 8 (or higher).
This section describes an example of setting up a MySQL server with docker. 
If you already have a MySQL server, you can skip this section.

## Setting Mysql database.

## Install G-CAT ID Manager
```sh
python setup.py install
```

## Requirement
mysql (8 or later)
pymysql
