# Connected Devices

| Device Name | IP Address | Connection Type | Ports (External:Internal) |
|-------------|------------|-----------------|--------------------------|
| Web/API Server | 192.168.1.43 | TCP | 5170:5173 (webserver), 3000:3000 (webapp), 3001:3001 (api), 4173:4173 (vite), 9000:9000 (webpack), 3003:3003 (nextjs), 7000-7020:7000-7020 (misc), 7021:80 (http), 7022:443 (https) |
| SSH Server | 192.168.1.43 | TCP | 6000:22, 6042:22 |
| HTTPS Server | 192.168.1.32 | TCP | 5321:3001, 4002:5371 |
| HTTP Server | 192.168.1.12 | TCP | 5320:3001 |
| SSH Ubuntu | 192.168.1.32 | TCP | 5600:22 |
| SSH Server 1 | 192.168.1.33 | TCP | 5375:22, 5372:4351 |
| SSH Server 2 | 192.168.1.40 | TCP | 5601:22 |
| SSH Server 3 | 192.168.1.44 | TCP | 5602:22 |
| Raspberry Pi 3B+ | 192.168.1.36 | TCP | 7050:22 |
