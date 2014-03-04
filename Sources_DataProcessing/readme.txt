Usage: 

Files: 
Place the pcap file you want to parse in the same directory as Rssi_Preprop.py (keep all other files in this directory as well). Add a second file to the directory with the same name as the pcap file, but with the prefix "flag_" (e.g. if you want to parse beispiel.pcap, add flag_beispiel.pcap). Write "new" to this file. After the pcap file is parsed once, this entry is automatically changed to "old", and you have to change it manually again, if you want to parse it a second time. The "flag_" file shall be used in future to signal the parser that new data was written to 
the pcap file.
If you don't need this feature for testing purposes, change the  corresponding "if.." statement in the main() method, but then the same pcap file will be parsed until you press "stop parsing".

Start program:
From console, go to the directory with Rssi_Preprop.py and call "python Rssi_Preprop.py"

Parsing:
Type in the name of the pcap file and choose the class for this data, then press "start parsing". To stop parsing, press "stop parsing". Note that if you not update the "flag_" file, the pcap file will be parsed at most once.

Adding new classes:
Adding a new class is only possible when the program is not parsing (i.e. start/stop button states "start parsing"). When you type in a new class, it is only used and stored if you press "add class to list" next. However, at the moment adding new classes is causing some trouble, so add all classes you're intending to use before you parse the first file.

Use parsed data:
The data can be accessed within the main class via self.data_table, which has the class Orange.data.Table. For more see comments in the code.

 