LAB 2
=====

This week you demonstrate that encryption alone is NOT security.

`FICAA <../FICAA.pdf>`_

`Classroom Slides <Lab2_classroom.pdf>`_


`Lab assignment <lab2.pdf>`_

Further Reading / Going Deeper
------------------------------

Reverse Engineering
...................

~5 years ago at DEFCON there was a presentation by a US Army Ranger where the presenter had made a reverse engineering tool (using Python) that could automatically recreate engineering units from raw data (he didn’t need to use a dictionary, like the excel file). His technology worked on ANY CANBUS, even those using completely proprietary message schemes.

* The presentation: https://www.youtube.com/watch?v=jh_H9LIvQIs (it is only 18 minutes long)
* Code on GitHub: https://github.com/brent-stone/CAN_Reverse_Engineering
 

A research team figured out how to reverse engineer *many* car CANBUS messages, without needing a car. They used mobile apps that were supposed to support the car owner.

* https://www.ndss-symposium.org/wp-content/uploads/2020/02/24231.pdf

Open-source tools that decode J1939? In general, those might be problematic since the SAE has a copyright on the dictionary.


SocketCAN
.........

Here is a video from 10 years ago at DEFCON “Vehicle Hacking Village” about SocketCAN:

* https://www.youtube.com/watch?v=Ym8xFGO0llY

In general, DEFCONs “Car Hacking Village” has good content. (also, apparently the village name changed over the last 10 years from “vehicle” to “car” hacking village)
