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

admin@ncs#
```
