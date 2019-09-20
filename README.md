[![Snap Status](https://build.snapcraft.io/badge/emiljoha/mpw.svg)](https://build.snapcraft.io/user/emiljoha/mpw) [![Build Status](https://travis-ci.com/emiljoha/mpw.svg?branch=master)](https://travis-ci.com/emiljoha/mpw)

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/mpw)

# Masterpassword

This is a linux commandline interface to the master password algorithm using an independent implementation of the algorithm.

Algorithm used developed by Maarten Billemont https://masterpassword.app so password generated with this cli is compatiple withe the wide variety of apps developed by the original author of the algorithm.

## Description

### What's your password?

Passwords are regarded as a "necessary evil" to having accounts online. We
accept them as "the way things are done online" and try to adapt.  But upon
reflection, we find that we've adapted quite poorly.

Sites everywhere expect us to come up with a secure and unique password for
them. But we're not security professionals. We do our best to compensate for
this unrealistic demand: to keep track of passwords, we reach for notebooks,
our computers, apps, or we simplify them so we won't forget.  We've become
symptomatic.

### The real issue.

Humans are no good at remembering lots of passwords. But writing them down or
saving them is dangerous, too.

Master Password avoids all the pitfalls: a cryptographic algorithm calculates
your site's password for you, only when you need it.  When you're done, it
erases the password from the device, so it can't be stolen.

Master Password's unique approach makes you safer from loss, theft, problems
with backups, sync, confiscation, snooping, and more.

## Getting started

### Snap

The easiest way to get mpw is to install the snap. The snap is only published
in edge and in development mode witch indicates that there might be
issues. But not more than in the other ways of installing the app.

```shell
sudo snap install --edge mpw --devmode

```

#### Build your own snap

Install lxd and snapcraft if you do not have them already.
``` shell
sudo snap install lxd && sudo /snap/bin/lxd init
sudo usermod -a -G lxd $USER && newgrp lxd
sudo snap install --classic snapcraft
```

Get the source code.
``` shell
git clone https://github.com/emijoha/mpw
```

Build the snap.
``` shell
cd mpw
snapcraft cleanbuild
```

### Build with setuptools

Install OpenSSL developmend packages.

OpenSuse
``` shell
sudo zypper in libopenssl-devel
```

Ubuntu
``` shell
sudo apt install libssl-dev
```

Install with setuptools
```shell
python3 setup.py install
```

To uninstall.
```shell
pip uninstall mpw
```

### Emacs

Install the snap and set FULL_NAME in the configuration JSON file.

The path of the file is shown when running. 


``` shell
mpw -h
```
You will need root priviliges to edit the config file.

Clone the mpw repo or just download the ```mpw.el``` file.

Add this to you emacs configuration.
``` elisp
(load-file "/path/to/mpw/mpw.el")
```

Run the command ```M-x mpw```. Write site name and password when promted. The
generated password will be in your clipboard.
