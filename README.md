serial_test
===========

This repository contains 2 python3 scripts - _sender.py_ and _receiver.py_, which can be used to test heavy serial communication
over USB serial port. Test is performed only in one direction at a time and integrity of data is not verified, only its count. 

### Context

This was created for testing of Gadget serial module.

* USB device - Beaglebone Black using _sender.py_
* USB host - PC using _receiver.py_
