barebone fedora-33 installation
=

After installing fedora-server you have to execute some changes on system level.
This document describes these changes.

## device specifications
* hardware : Gigabyte GB-BXBT-2807
* operating system : fedora-33-server


## resize your lvm
After installing fedora-33 the disksize is by default set to 15Gb.
The actual harddisk size is 250Gb

As root execute the following commands to reclaim the addition disk space:
```shell
$ lvextend /dev/mapper/fedora_snapsnare-root -l+100%FREE
$ xfs_growfs /dev/mapper/fedora_snapsnare-root
```

## install git
As root execute the following command
```shell
$ dnf install git
```