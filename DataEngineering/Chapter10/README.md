# FinMindBook 10 - Traefik 與 API 部署

本章以 traefik 作為反向代理（reverse proxy），
將 FastAPI 服務部署到 Docker Swarm 上對外提供，
並由 traefik 處理 http/https 導向、SSL 憑證與 loading balance。

## 章節目錄

| 小節 | 主題 |
| --- | --- |
| [10.4](10.4) | 部署 traefik，建立 traefik-public overlay network |
| [10.5](10.5) | 將 FastAPI 服務搭配 traefik 部署上線（程式與設定見 10.5/api） |
