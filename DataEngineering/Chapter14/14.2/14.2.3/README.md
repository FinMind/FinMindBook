# FinMindBook 14.2.3 - Netdata

本節用 docker compose 在單機啟動 netdata，
監控機器的硬體資源（CPU、記憶體、磁碟、網路等）。

## 啟動 netdata
    docker compose -f netdata.yml up -d

瀏覽器開啟 http://localhost:19999
