# nasdaq_itch_pcap
Experiments with PCAP files from NASDAQ's public FTP server 

## Overview: Source Files, Format 
NASDAQ offers sample PCAP files at **ftp://emi.nasdaq.com/ITCH/** (herein "root" or "~/"). This link can be opened in a file browser. Several variants are available, based on [the different NASDAQ data feeds](https://nasdaqtrader.com/Trader.aspx?id=dpspecs): 
- NASDAQ ITCH 5.0 (any *.NASDAQ_ITCH_50.gz file in root or ~/Nasdaq_ITCH/)
  - Protocol: [Nasdaq TotalView-ITCH 5.0](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf) [1]
- BX ITCH 5.0 (any *.BX_ITCH_50.gz file in root or ~/BX_ITCH/)
  - Protocol: [BX TotalView-ITCH 5.0](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/BXTVITCHSpecification.pdf)
- PSX ITCH 5.0 (any *.PSX_ITCH_50.gz file in root or ~/PSX_ITCH/)
  - Protocol: [PSX TotalView-ITCH 5.0](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/PSXTVITCHSpecification.pdf)


The PCAP files in these GZ archives don't follow the standard [libpcap format](https://gitlab.com/wireshark/wireshark/-/wikis/Development/LibpcapFileFormat) (no global header, etc.). Instead, they follow [NASDAQ's BinaryFILE format](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/binaryfile.pdf): each PCAP is a just a binary file with order-by-order data for the trading session indicated in the filename. There are no headers, each file is just a set of *messages*, where each message has a length field and a payload field:<br>
![image](https://user-images.githubusercontent.com/18313961/124309418-afdbc800-db38-11eb-9302-c286c5d1c59c.png)



## Wireshark
The PCAPs can be opened in Wireshark using one of Open Markets Initiative's [Lua](https://gitlab.com/wireshark/wireshark/-/wikis/Lua/) dissector scripts:
1. [NASDAQ ITCH 5.0](https://github.com/Open-Markets-Initiative/wireshark-lua/blob/master/Nasdaq/Nasdaq.Equities.TotalView.Itch.v5.0.Script.Dissector.lua)
2. [BX ITCH 5.0](https://github.com/Open-Markets-Initiative/wireshark-lua/blob/master/Nasdaq/Nasdaq.Bx.Equities.TotalView.Itch.v5.0.Script.Dissector.lua)
3. [PSX ITCH 5.0](https://github.com/Open-Markets-Initiative/wireshark-lua/blob/master/Nasdaq/Nasdaq.Psx.TotalView.Itch.v5.0.Script.Dissector.lua)

Download the Lua scripts, then in Wireshark, click Help –> About Wireshark –> Folders: place the downloaded files in the directory corresponding to "Personal Lua Plugins". After placing the Lua scripts there, click Analyze -> Reload Lua Plugins. Then, click Analyze -> Enabled Protocols. A search for "itch" should return entries for the 3 TotalView ITCH dissectors.

Unfortunately, I'm not able to open the PCAPs using these dissectors, but I've filed a [github issue](https://github.com/Open-Markets-Initiative/wireshark-lua/issues/29) for clarification


## Python
In the files I've looked at, the payload length for the first message is 0x000c. This is is the Code "O" System Event Message [1, Sect. 4.1] to indicate the trading session is starting.
