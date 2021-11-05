snapsnare
=

snapsnare, this project, the platform where musicians meet, share and create compositions.

Table of contents:

* Remarks
* Getting started
  * General installation (non-production)
  * Development installation

# Remarks
snapsnare currently supports Python 3.5 and higher.

# Getting started
snapsnare consists of 2 parts, a flask web application and a postgresql database.
When you want to use snapsnare it is recommended that you follow the instructions described in the general installation section.


## General installation
snapsnare depends on the snapsnare database. 
Before you start the installation of snapsnare it is recommended you execute these [installation instructions](https://github.com/janripke/snapsnare-db/blob/main/README.md) first.

### configure snapsnare
For safety reasons the snapsnare database credentials are stored on your local machine. 
To be more exact under ~/.snapsnare/snapsnare-ds.json

create the snapsnare-ds.json in ~/.snapsnare folder: paste the following into this file:
```python
{
  "type": "postgresql",
  "host": "localhost",
  "db": "snapsnare",
  "username": "snapsnare_owner",
  "password": "snapsnare_owner"
}
```

### install dependencies
For converting m4a to wav, snapsnare uses pydub. This package dependend on the ffmpeg library.
Install ffmpeg through executing, as root, the following command:
```shell
sudo dnf install ffmpeg 
```

### install snapsnare
```shell
pip3 install git+https://github.com/janripke/snapsnare.git@0.0.10#egg=snapsnare
```

### run snapsnare
```shell
snapsnare
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
2021-01-11 00:07:40,788 werkzeug INFO _internal _log:113 -  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```


## Development installation
snapsnare depends on the snapsnare database. 
Before you start the installation of snapsnare it is recommended you execute these [installation instructions](https://github.com/janripke/snapsnare-db/blob/main/README.md) first.

### configure snapsnare
For safety reasons the snapsnare database credentials are stored on your local machine. 
To be more exact under ~/.snapsnare/snapsnare-ds.json

create the snapsnare-ds.json in ~/.snapsnare folder: paste the following into this file:
```python
{
  "type": "postgresql",
  "host": "localhost",
  "db": "snapsnare",
  "username": "snapsnare_owner",
  "password": "snapsnare_owner"
}
```

### clone snapsnare
```
git clone https://github.com/janripke/snapsnare.git
```

### run snapsnare
```shell
python3 snapsnare/app.py
```



