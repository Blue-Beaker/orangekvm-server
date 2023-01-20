# OrangeKVM-server

[中文](README_cn.md)  
An simple ipkvm server with web interface. Made for orangepi zero, also usable on other linux devices.  

Uses CH9329 chip to control keyboard and mouse.  
<b>Don't expose the server to public network without extra encryption.  </b>

USB storage emulation: This server can use [USB Gadget Mass Storage](https://linux-sunxi.org/USB_Gadget/Mass_storage) to emulate a bootable USB drive.  
1. make sure your user running the server is able to `sudo modprobe g_mass_storage` with no password, or it will fail.  
2. Put images in `usbimages` folder. Images can be ISO(read-only) and raw image(read-write, can be created with `dd` command).  
3. Select the image from the dropdown menu in the web interface and click "load"  
Note: Other loaded USB Gadget modules may interference with this.

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