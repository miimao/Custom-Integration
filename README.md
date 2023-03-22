Note: Despite this running in production with minimal hickups I would not recomend others use this project. It was made in freetime to try and leverage the python skills I was still developing and have since decided this could be re writen to be much more effective and resliant to failure.

As my first real project im going to keep it up but as an archive and a reminder of humble begings.

# CTC-Custom-Integration
Custom Integration for Domotz and ConnectWise Manage.

The program is designed to automate the process of keeping device configurations up-to-date in Connectwise Manage based on changes detected by Domotz network monitoring. The program achieves this by leveraging the APIs provided by both Connectwise Manage and Domotz.

When the program is launched, it establishes a connection to both Connectwise Manage and Domotz. It then scans the network for devices and retrieves their configuration information from Domotz. The program then compares this information with the existing device configurations in Connectwise Manage and makes any necessary updates or additions.

Whenever a new device is added to the network, the program automatically creates a new configuration record in Connectwise Manage. Similarly, when a device is removed from the network, the program removes its configuration from Connectwise Manage.

In addition to keeping device configurations up-to-date, the program also automatically assigns devices to tickets that are opened by Domotz. Whenever a new ticket is created in Domotz, the program checks to see if any of the affected devices are already in Connectwise Manage. If so, it assigns the ticket to the corresponding device in Connectwise Manage.

The program is designed to run continuously in the background, periodically checking for updates and changes.
