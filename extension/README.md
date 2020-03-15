gopaccli
========

gopaccli - консольная утилита вычисляющая прокси необходимый для доступа к 
заданному ресурсу.

**Пример использования**

```
>>> gopaccli -pacPath https://antizapret.prostovpn.org/proxy.pac -url http:/filmix.me
{"Proxy":{"http":"http://proxy.antizapret.prostovpn.org:3128","https":"http://proxy.antizapret.prostovpn.org:3128"},"Error":""}

>>> gopaccli -pacFile https://antizapret.prostovpn.org/proxy.pac -url http://google.com
{"Proxy":{},"Error":""}
```
