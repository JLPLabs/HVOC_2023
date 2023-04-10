LAB 8
=====

Using proof-of-possession tokens for ECU authorization.

HINT: need to install cwt...

.. code-block:: bash

  $ sudo pip3 install cwt

`FICAA <../FICAA.pdf>`_

`Classroom Slides <Lab8_classroom.pdf>`_

`Lab assignment <lab8.pdf>`_

ISO-TP Issues??
----------------

You may have issues with the Azure VM when running the transfer protocol examples.

For some reason the *can_isotp* module isn't included in our kernel and when you try to build it from source code the **Make** process refuses to comply, instead it complains bitterly that there is no reason for you to be building this module as it is already installed.

Hmmm...

Solution
........

1. Get the source code from: https://github.com/hartkopp/can-isotp

2. Comment out lines 92-94 from can-isotp/net/can/isotp.c (which disables the check)

3. Build and install the module

.. code-block:: bash

  $ make                        # generates some errors; feel free to ignore them
  $ sudo make modules_install
  
  $ sudo modprobe can
  $ sudo insmod ./net/can/can-isotp.ko

Test
....

Get into the lab8 'bench' directory.::

  $ ./setup_fd_vcan.sh
  $ lsmod | grep can
  vcan                   16384  0
  can_isotp              24576  0
  can                    24576  1 can_isotp
 
Terminal 1::

  $ isotprecv -s 40 -d 30 -l vcan0
 
Terminal 2::

 $ candump vcan0
  
Terminal 3::

  $ echo 11 22 33 44 55 66 CA FE 99 AA | isotpsend -s 30 -d 40 vcan0
 
Terminal 2 gets::

  vcan0  030   [8]  10 0A 11 22 33 44 55 66
  vcan0  040   [3]  30 00 00
  vcan0  030   [5]  21 CA FE 99 AA
 
Terminal 1 gets::

  11 22 33 44 55 66 CA FE 99 AA
 
 
