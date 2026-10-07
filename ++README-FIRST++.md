
## Which Application should I use? ##

- There are 2 Applications in the archive; **NodeBox\_arm.app** and **NodeBox\_intel.app**. Despite their names, **NodeBox\_arm** may be usable by Intel Macs - I just don't know the minimal OS version. My guess would be 10.15... but I dont have the machines to try.

- Try the **ARM** version first. If it crashes fall back to the **INTEL** version.

- The **INTEL** version should work on OSX 10.13 and up.


## What should I do first? ##

- Launch the application & open the preferences.

- Set the Library folder to the one in the archive

- Quit the Application.

- Launch the app again.

- open and run the script **Library/linguistics/DOWNLOAD\_DATABASES\_AND\_INSTALL\_CONCEPTNET.py**

	- This downloads and initializes some databases needed all over the Library folders.

	- The runtime is about 4 minutes on a M-1 and 8.5 minutes on an i5.

- you're done. Try out the examples and have fun.


