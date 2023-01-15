# OrangeKVM-server

[English](README.md)  
使用网页界面的简易ipkvm服务端。针对orangepi zero开发,也可在其他Linux设备上使用。

使用 CH9329 芯片控制键盘鼠标。  
<b>不要在没有额外加密的情况下将此服务端暴露在公网。  </b>

配置:  
`[server]`:  
`address`: 服务端监听地址.  
`port`: 网页界面端口.  
`wsport`: Websocket端口.  

`[stream]`:  
`stream_url`: MJPG 串流地址。需要串流服务端，如ustreamer.   

`[hid]`:  
`hid_type`:   
- `ch9329`: ch9329 协议传输  

`serial_path`: 
- 串口路径, 如 `/dev/ttyUSB0`.
- 或 TCP串口 `tcp://主机:端口`, 如 `tcp://192.168.1.2:23`


`ch9329_address`:  
- ch9329 芯片地址，十进制格式. 默认为 0.  

`baudrate`:  
- 当使用本地串口: 串口波特率.  
- 当使用TCP串口: 不使用, 请在TCP串口主机设置波特率.  