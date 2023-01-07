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
- `ch9329_tty`: ch9329 over serial  
- `ch9329_tcp`: ch9329 over serial over tcp  

`hid_path`: 
- When using `ch9329_tty`: serial port path, for example `/dev/ttyUSB0`.
- When using `ch9329_tcp`: serial over tcp host:port, for example `192.168.1.2:23`


`ch9329_address`:  
- ch9329 chip address in decimial format. defaults to 0.  

`baudrate`:  
- When using `ch9329_tty`: serial port baudrate.  
- When using `ch9329_tcp`: unused, please set baudrate on your serial-over-tcp host instead.  