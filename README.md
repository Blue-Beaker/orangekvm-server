# OrangeKVM-server

[中文](README_cn.md)  
An simple ipkvm server with web interface. Made for orangepi zero, also usable on other linux devices.  

Uses CH9329 chip to control keyboard and mouse.  
<b>Don't expose the server to public network without extra encryption.  </b>

Configuration:  
`[server]`:  
`address`: Server listen address.  
`port`: Web interface port.  
`wsport`: Websocket port.  

`[stream]`:  
`stream_url`: MJPG streaming url. a streaming server is needed, for example ustreamer.   

`[hid]`:  
`hid_type`:   
- `ch9329`: ch9329 protocol

`serial_path`: 
- serial port path, for example `/dev/ttyUSB0`.  
- or serial over tcp: `tcp://host:port`, for example `tcp://192.168.1.2:23`  


`ch9329_address`:  
- ch9329 chip address in decimial format. defaults to 0.  

`baudrate`:  
- When using local serial: Serial port baudrate. 
- When using serial over tcp: Unused , please set baudrate on your serial-over-tcp host instead.  