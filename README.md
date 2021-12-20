G-CAT ID Manager
==================

# Intoroduction
G-CAT ID Manager is a tool that stores readable IDs (like ID00001) and UUIDs (like aaaaaaaa-1111-4bbb-r222-cccccccccccc) in MySQL database, and support conversion.
It is designed for cancer genome analysis, but can be used for any system that needs to convert between readble IDs and UUIDs.

# Installation
## Setting MySQL server
1. Install and configure MySQL Server 8 or higer. It is recommended to use Docker.
https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/docker-mysql-getting-started.html

2. Access MySQL server as root.
```
mysql -u root -p
```

3. Create database.
```
CREATE DATABASE your_database;
```

4. Create table. "sample_uuid" and "sample_name" colmuns required.
```
USE your_database;
CREATE TABLE ID NOT EXISTS your_table(
    `id` INT NOT NULL AUTO_INCREMENT,
    `sample_uuid` VATBINARY(16) NOT NULL,
    `sample_name` VARCHAR(256) NOT NULL,
    some other colmuns...
);
```

5. Create read-only user and set access privileges.
```
CREATE USER your_user IDENTIFIED BY "your password";
GRANTS SELECT ON your_database.* to "your_user"@"%";
```

## Install G-CAT ID Manager
```sh
python setup.py install
```

## Requirement
mysql (8 or later)
pymysql
