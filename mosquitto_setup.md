# Mosquitto Server Setup

## On EC2 instance
1. Install mosquitto and mosquitto client
```
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
```

2. Create `/etc/mosquitto/conf.d/default.conf`
- Include the following:
```
allow_anonymous true

listener 1883 0.0.0.0
```

3. Restart mosquitto
```
sudo systemctl restart mosquitto
```

4. Confirm listening on port 1883
```
netstat -lntu
```
Sample output:
```
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:1883            0.0.0.0:*               LISTEN     
tcp6       0      0 :::22                   :::*                    LISTEN
```

## API Server & Mosquitto Server Security Group
- Add inbound rules from each MQTT Client
  1. MQTT Access 
    * Type: `Custom TCP`
    * Port: `1883`
    * Source: `<client_public_ipv4>`
  2. API Server Access
    * Type: `HTTP`
    * Port: `80`
    * Source: `<client_public_ipv4>`
- Add inbound rule from laptop/desktop
  * Type: `SSH`
  * Port: `22`
  * Source: `<user_public_ipv4>`

## MQTT Client Security Group
- Add inbound rule for ssh access
  * Type: `SSH`
  * Port: `22`
  * Source: `<user_public_ipv4>`
- Use same security group for all clients
