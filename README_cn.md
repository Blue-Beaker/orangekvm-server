# OrangeKVM-server

[English](README.md)  
使用网页界面的简易ipkvm服务端。针对orangepi zero开发,也可在其他Linux设备上使用。

使用 CH9329 芯片控制键盘鼠标。  
<b>不要在没有额外加密的情况下将此服务端暴露在公网。  </b>

USB存储模拟: 此服务端可利用 [USB Gadget Mass Storage](https://linux-sunxi.org/USB_Gadget/Mass_storage) 来模拟可启动的USB盘.  
1. 确保运行此服务端的用户可以免密码执行 `sudo modprobe`, 否则无法模拟.  
2. 将镜像放在 `usbimages` 文件夹内. 镜像格式可以是ISO(只读) 或原始磁盘映像(读写, 可使用 `dd` 命令创建).  
3. 在网页界面的下拉框中选择需要的镜像文件, 然后点击 "load"  
注意：其他已加载的USB Gadget模块可能影响此功能的使用

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