# nasdaq_itch_pcap
Experiments with PCAP files from NASDAQ's public FTP server 

## Overview 
NASDAQ offers sample PCAP files at **ftp://emi.nasdaq.com/ITCH/** (herein "root" or "~/").<br>This link can be opened in a file browser. The PCAP files are in binary format and they represent order by order data for the trading day indicated in the filename. Several variants are available, based on [the different NASDAQ data feeds](https://nasdaqtrader.com/Trader.aspx?id=dpspecs): 

<ol>
<li>NASDAQ ITCH (any *.NASDAQ_ITCH_50.gz file in root or ~/Nasdaq_ITCH/)
    <ul>The associated protocol specification is Nasdaq TotalView-ITCH 5.0  </ul>
<ul>https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf</ul>
  </li>
<li>BX ITCH (any *.BX_ITCH_50.gz file in root or ~/BX_ITCH/)
    <ul>The associated protocol specification is BX TotalView-ITCH 5.0  </ul>
<ul>https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/BXTVITCHSpecification.pdf</ul>
  </li>
<li>PSX ITCH (any *.PSX_ITCH_50.gz file in root or ~/PSX_ITCH/) </li>
    <ul>The associated protocol specification is PSX TotalView-ITCH 5.0</ul>
<ul>https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/PSXTVITCHSpecification.pdf</ul>
  
</ol>

Currently, I'm just focusing on the NASDAQ ITCH files. They do not follow [the libpcap format](https://gitlab.com/wireshark/wireshark/-/wikis/Development/LibpcapFileFormat).
