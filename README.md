# Anomaly Network Detection
Introduction
       Viasat Inc. is an American communications company that provides high-speed satellite broadband services and secure networking systems covering military and commercial markets. Therefore, ensuring high quality network performance is crucial for maintaining customer satisfaction. Fundamental factors that affect network performance are packet loss and latency.

       Small units of data that are sent and recieved across a network are called packets, and packet loss occurs when one or more of these packets fails to reach its intended destination. Latency is the delay between a user's action and a web application's response to that action. High quantities of each of these often results in slow service and network disruptions for the user.

       The problem we are trying to explore is: can we detect anomalies within network traffic, whether it be an increase in the packet loss rate, larger latency, or both? Packet loss can be caused by a number of issues, including: network congestion, problems with network hardware, software bugs and security threats. On the other hand, main factors that affect network latency are: the transmission medium (copper cable-based networks vs. modern optic fibers), propagation (how far apart the networks are), efficiency of routers and storage delays.

       The ability to detect anomalies on a data stream would be extremely useful as it can be an effective monitoring & alerting system for poor network conditions. If an anomaly is predicted, our hope is that a proper recovery protocol can be put in place to stabilize network performance, creating a better experience for the end user.

Methodology
The Data
We will be using data generated from DANE (Data Automation and Network Emulation Tool), a tool that automatically collects network traffic datasets in a parallelized manner without background noise, and emulates a diverse range of network conditions representative of the real world. Using DANE, we are able to configure parameters such as latency and the packet loss ratio ourselves. More importantly, we are able to simulate an anomaly by changing the configuration settings of the packet loss rate and latency mid run. The data collected is already aggregated per second with these fields:

DANE Features	Description
Time	Broken down into seconds(epoch)
Port 1 & 2	Identifier of where the packets are being sent to and from. Can originate from either
IP	IP address of the ports in comunication
Proto	IP Protocol number that identifies the transport protocol for the packet
Port 1->2 Bytes	Total bytes sent from port 1 to 2 in given second
Port 2->1 Bytes	Total bytes sent from port 2 to 1 in given second
Port 1->2 Packets	Total packets sent from port 1 to 2 in given second
Port 2->1 Packets	Total packets sent from port 2 to 1 in given second
Packet_times	Time in milliseconds that the packet arrived
Packet_size	Size of the bytes of the packet
Packet_dirs	Which endpoint was the source of each packet that arrived


       We ran only two scenarios at once to prevent overloading our CPU by running too many DANE scenarios concurrently. Each DANE run is 5 minutes long. The configuration change happens at the 180 second mark and what we configure for our packet loss rate determines the likelihood of each packet being dropped. This way, we are able to simulate an anomaly within our data and are able to simulate packet loss in a more realistic manner. Our steady state had a packet loss ratio of 1/5,000 and a latency of 40 ms. We are focused on identifying changes of a factor of 4 and above. In our case a packet loss ratio of 1/1,250 and a latency of 160 ms or greater or a packet loss ratio of 1/20,000 and latency of 10 ms.
