# Decription

py_cli : NSO Action Package of live-status for NETCONF NED device (CLI NED device as well)
          
- python code using paramiko
 
- reading the host/account/ssh information from CDB
          



# Checking the device's NED
```
admin@ncs# show devices list
NAME   ADDRESS          DESCRIPTION  NED ID                ADMIN STATE
------------------------------------------------------------------------
cat3k  10.62.149.24     -            cisco-ios-cli-6.74    unlocked
cat9k  10.70.137.4      -            cisco-ios-cli-6.74    unlocked
junos  192.168.124.117  -            juniper-junos-nc-4.6  unlocked
```



# Checking the Package info
```
admin@ncs# show packages package oper-status
                          PROGRAM                                                                       META     FILE
                          CODE     JAVA           PYTHON         BAD NCS  PACKAGE  PACKAGE  CIRCULAR    DATA     LOAD   ERROR
NAME                  UP  ERROR    UNINITIALIZED  UNINITIALIZED  VERSION  NAME     VERSION  DEPENDENCY  ERROR    ERROR  INFO
------------------------------------------------------------------------------------------------------------------------------
cisco-ios-cli-6.74    X   -        -              -              -        -        -        -           -        -      -
juniper-junos-nc-4.6  X   -        -              -              -        -        -        -           -        -      -
py_cli                X   -        -              -              -        -        -        -           -        -      -
```


# Example of calling the py_cli action onto the Netconf NED device

- target device : Olive Junos virtual swtich on the GNS3 VM

```
admin@ncs# py_cli:action exec device junos command "show configuration"
result ## Last commit: 2022-01-05 09:11:35 UTC by admin
version 12.1R1.9;
system {
    root-authentication {
        encrypted-password "$1$jjGK..Gq$e.LZSLErhIiVvJFLLsznv1"; ## SECRET-DATA
    }
    login {
        user admin {
            uid 2000;
            class super-user;
            authentication {
                encrypted-password "$1$AXMncrZ6$ge5P0Xl55EshlhukQponV0"; ## SECRET-DATA
            }
        }
    }
    services {
        ssh;
        netconf {
            ssh {
                port 830;
            }
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
interfaces {
    em0 {
        enable;
        unit 0 {
            family inet {
                address 192.168.124.117/24;
            }
        }
    }
}

admin@ncs# py_cli:action exec device junos command "show ver"
result Model: olive
JUNOS Base OS boot [12.1R1.9]
JUNOS Base OS Software Suite [12.1R1.9]
JUNOS Kernel Software Suite [12.1R1.9]
JUNOS Crypto Software Suite [12.1R1.9]
JUNOS Packet Forwarding Engine Support (M/T Common) [12.1R1.9]
JUNOS Packet Forwarding Engine Support (M20/M40) [12.1R1.9]
JUNOS Online Documentation [12.1R1.9]
JUNOS Voice Services Container package [12.1R1.9]
JUNOS Border Gateway Function package [12.1R1.9]
JUNOS Services AACL Container package [12.1R1.9]
JUNOS Services LL-PDF Container package [12.1R1.9]
JUNOS Services PTSP Container package [12.1R1.9]
JUNOS Services Stateful Firewall [12.1R1.9]
JUNOS Services NAT [12.1R1.9]
JUNOS Services Application Level Gateways [12.1R1.9]
JUNOS Services Captive Portal and Content Delivery Container package [12.1R1.9]
JUNOS Services RPM [12.1R1.9]
JUNOS Services HTTP Content Management package [12.1R1.9]
JUNOS AppId Services [12.1R1.9]
JUNOS IDP Services [12.1R1.9]
JUNOS Services Crypto [12.1R1.9]
JUNOS Services SSL [12.1R1.9]
JUNOS Services IPSec [12.1R1.9]
JUNOS Runtime Software Suite [12.1R1.9]
JUNOS Routing Software Suite [12.1R1.9]

admin@ncs# py_cli:action exec device junos command "show interface em0"
result Physical interface: em0, Enabled, Physical link is Up
  Interface index: 8, SNMP ifIndex: 17
  Type: Ethernet, Link-level type: Ethernet, MTU: 1514, Speed: 1000mbps
  Device flags   : Present Running
  Interface flags: SNMP-Traps
  Link type      : Full-Duplex
  Current address: 0c:84:cc:01:00:00, Hardware address: 0c:84:cc:01:00:00
  Last flapped   : 2022-01-05 09:07:29 UTC (03:11:58 ago)
    Input packets : 1700
    Output packets: 1360

  Logical interface em0.0 (Index 67) (SNMP ifIndex 18)
    Flags: SNMP-Traps Encapsulation: ENET2
    Input packets : 1706
    Output packets: 1369
    Protocol inet, MTU: 1500
      Flags: Sendbcast-pkt-to-re, Is-Primary
      Addresses, Flags: Is-Default Is-Preferred Is-Primary
        Destination: 192.168.124/24, Local: 192.168.124.117, Broadcast: 192.168.124.255

admin@ncs#
```
