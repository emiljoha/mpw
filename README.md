[![Snap Status](https://build.snapcraft.io/badge/emiljoha/mpw.svg)](https://build.snapcraft.io/user/emiljoha/mpw)

# Masterpassword

This is a linux commandline interface based on the https://masterpassword.app/
platform independent cli by Maarten Billemont. The c code implementing the
masterpassword algorithm is identical to the official version.

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

The easiest way to get mpw is to install the snap. At the moment the
snap does not support settings or copy paste but it will soon
(hopefully). Due to this unfinished state the snap is only published
in edge and in development mode. 

```shell
sudo snap install --edge mpw-emijoh --devmode


### Build with setuptools

Building the C/C++ libraries have dependencies boost_system,
boost_filesystem, boost_python and libsodium.

#### Dependencies on mac

```shell
brew install boost python3 libsodium boost-python3
````
#### Dependencies on Linux

TODO (you can find the dependenices for ubuntu16.04 in the snap/snapcraft.yaml)


After installing dependencies build and install with.

```shell
	python3 setup.py build
	python3 setup.py install
```

To uninstall.

```shell
	pip uninstall mpw
```





