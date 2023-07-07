# FreeGPT WebUI by Neurogen

* Улучшенные официальные образы для докера.
* Improved official docker images.

* Все образы теперь запускаются с помощью `supervisord`, а не одиночных  `CMD python3 ./run.py` или `CMD python3 ./entrypoint.py`.
* Начиная с версии `v1.3+` образы теперь содержат **оба** приложения в фоне - `webui` чат (на порту `1338`) и `endpoint` api (на порту `1337`).

* All versions now running by `supervisord` instead of direct `CMD python3 ./run.py` or `CMD python3 ./entrypoint.py`
* Since `v1.3+` image contain **both** applications in background - `webui` chat (via port `1338`) and `endpoint` api (via port `1337`).

# Готовый пример для запуска через docker-compose \\ Ready docker-compose example

```yml
version: "3.9"
services:
  freegpt-webui:
    image: neurogendev/freegpt:latest #1.3.2, <...>, 1.0, etc
    container_name: freegpt
    hostname: freegpt
    restart: always
    ports:
       - 1337:1337
       - 1338:1338
```

