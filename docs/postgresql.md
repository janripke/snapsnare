postgresql database installation
=

This document describes the creation of the snapsnare database in the postgresql server.
It is assumed that the postgresql server is installed and running.

## check the status of the postgresql server

1. login as root:

```shell script
# login as root
$ sudo -i
```

2. when root login as the postgres user:

```shell script
$ su - postgres
```

3. connect to the postgresql server
```shell script
$ psql
```


## create the snapsnare database
This section describes the actual creation of the snapsnare database in the postgresql server
It is assumed you are connected to postgresql database, see previous section

execute the following commands in the postgresql server
```
postgres=# create database snapsnare encoding 'utf8';
postgres=# create user snapsnare_owner with encrypted password 'snapsnare_owner' login ;
postgres=# grant all privileges on database snapsnare to snapsnare_owner;
```

disconnect from the postgresql server
```shell script
postgres=# \q
```

## connect to the snapsnare database

```shell script
$ PGPASSWORD=snapsnare_owner psql --host=localhost --username=snapsnare_owner --dbname=snapsnare
```

## install the uuid-ossp module
The uuid-ossp module is used to generate uuid's

1. login as root:

```shell script
# login as root
$ sudo -i
```

2. when root login as the postgres user:

```shell script
$ su - postgres
```

3. install the uuid-ossp module in the snapsnare database
```shell script
$ psql -d snapsnare -c 'create extension "uuid-ossp";' 
```

4. check as normal user if the module is installed
```shell script
$ PGPASSWORD=snapsnare_owner psql --host=localhost --username=snapsnare_owner --dbname=snapsnare
postgres=# select * from pg_extension;
```

## other postgresql commands

* switch database : \c
* show databases  : \l
* show tables     : \dt
* show users      : \du
* exit            : \q
  

