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

4. Create table. "sample_uuid" and "sample_name" columns required.
```
USE your_database;
CREATE TABLE ID NOT EXISTS your_table(
    `id` INT NOT NULL AUTO_INCREMENT,
    `sample_uuid` VARBINARY(16) NOT NULL,
    `sample_name` VARCHAR(256) NOT NULL,
    some other columns...
);
```

5. Create read-only user and set access privileges. This user is used to display the IDs and UUIDs. Note that the password should be set to something that can be shared within the system you are using.
```
CREATE USER your_user IDENTIFIED BY "your_password";
GRANT SELECT ON your_database.* TO "your_user"@"%";
```

6. Create adimn user and set access privileges. This user is used to INSERT IDs and manage the databases. Note that this password will not be shared.
```
CREATE USER your_admin_user IDENTIFIED BY "your_admin_password";
GRANT ALL ON your_database.* TO "your_admin_user"@"%";
```

## Install G-CAT ID Manager
```sh
python setup.py install
```

## Requirement
* mysql-server (8 or later)
* Python 3.8
* pymysql

# Usage
## Insert ID into Database
1. Access MySQL server as admin user.
```
mysql -u your_admin_user -p 
```

2. Insert the combination of readable ID and UUID. The following is an example of inserting the combination of redable ID "ID00001" and UUID "aaaaaaaa-1111-4bbb-2222-cccccccccccc". Note that the UUID must be converted from STRING to BINARY.
```
INSERT IGNORE INTO your_table (`sample_uuid`, `sample_name`) VALUES (UUID_TO_BIN("aaaaaaaa-1111-4bbb-2222-cccccccccccc"), "ID00001");
```

## Display ID 
0. Write the connection informatino to MySQL in the config file.
```
cat example_my.cnf
[client]
host = Your database server
user = Your MySQL user
port = Your MySQL server port number
database = Your database name
password = Yout database password
```

You can connect to MySQL by specifying this file with `-c` option of the gcat_uuid command.
```
gcat_uuid -c example_my.cnf
```

If not spcefied `-c` option, `~/.my.cnf` will be used.
If you do not want to write the password in the config file, you can use `-p` option to enter the password interactively 

1. Convert UUID to readable ID.
```
gcat_uuid -c example_my.cnf -u aaaaaaaa-1111-4bbb-2222-cccccccccccc
ID00001
```

2. Convert readable ID to UUID.
```
gcat_uuid -c example_my.cnf -n ID00001
aaaaaaaa-1111-4bbb-2222-cccccccccccc
```
