# generateLogReport
Генератор отчета лог файла **opencart**
## Описание
Утилита позволяет получить отчет по следующим показателям:

1. общее количество выполненных запросов
2. количество запросов по типу: GET - 20, POST - 10 и т.п.
3. топ 10 IP адресов, с которых были сделаны запросы
4. топ 10 самых долгих запросов, должно быть видно метод, url, ip, время запроса
5. топ 10 запросов, которые завершились клиентской ошибкой, должно быть видно метод, url, статус код, ip адрес
6. топ 10 запросов, которые завершились ошибкой со стороны сервера, должно быть видно метод, url, статус код, ip адрес

используя в качестве источника файл лога приложения opencart
## Запуск
`python genScript.py --logdir D:\generateLogReport` - выполнит поиск файлов с расширением `.log` в директории `--logdir` и на их основе сформирует отчет

`python genScript.py --logfile D:\generateLogReport\access.log` - выполнит поиск файла `--logfile` и на его основе сформирует отчет

Отчет сформируется в формате json

Пример отчета:
```
{
    "count_requests": 616,
    "count_by_type_requests": {
        "GET": 168,
        "POST": 122,
        "Head": 1
    },
    "top_ip": {
        "191.182.199.16": 13,
        "188.45.108.168": 31,
        "83.167.113.100": 8,
        "188.123.230.195": 8,
        "109.252.11.47": 6,
        "94.233.147.245": 6,
        "188.123.230.196": 5,
        "95.140.24.131": 4,
        "46.72.184.174": 4,
        "178.44.144.231": 4,
        "95.153.132.103": 4,
        "5.140.164.122": 4
    },
    "the_longest_requests": [
        {
            "type_req": "GET",
            "url": "/images/bg_raith.jpg",
            "ip": "191.182.199.16",
            "duration": 329961
        },
        {
            "type_req": "GET",
            "url": "/images/bg_raith.jpg",
            "ip": "188.45.108.168",
            "duration": 329961
        },
        {
            "type_req": "GET",
            "url": "/images/bg_raith.jpg",
            "ip": "191.182.199.16",
            "duration": 329961
        },
        {
            "type_req": "GET",
            "url": "/images/bg_raith.jpg",
            "ip": "188.45.108.168",
            "duration": 329961
        },
        {
            "type_req": "GET",
            "url": "/images/stories/slideshow/almhuette_raith_07.jpg",
            "ip": "188.45.108.168",
            "duration": 94861
        },
        {
            "type_req": "GET",
            "url": "/images/stories/slideshow/almhuette_raith_07.jpg",
            "ip": "191.182.199.16",
            "duration": 94861
        },
        {
            "type_req": "GET",
            "url": "/images/stories/slideshow/almhuette_raith_07.jpg",
            "ip": "188.45.108.168",
            "duration": 94861
        },
        {
            "type_req": "GET",
            "url": "/images/stories/slideshow/almhuette_raith_01.jpg",
            "ip": "191.182.199.16",
            "duration": 88161
        },
        {
            "type_req": "GET",
            "url": "/images/stories/slideshow/almhuette_raith_01.jpg",
            "ip": "188.45.108.168",
            "duration": 88161
        },
        {
            "type_req": "GET",
            "url": "/images/stories/slideshow/almhuette_raith_01.jpg",
            "ip": "191.182.199.16",
            "duration": 88161
        }
    ],
    "top_client_error_key_report": {
        "404": [
            {
                "type_req": "GET",
                "url": "/templates/_system/css/general.css",
                "status": 404,
                "ip": "188.45.108.168"
            },
            {
                "type_req": "GET",
                "url": "/favicon.ico",
                "status": 404,
                "ip": "188.45.108.168"
            }
        ]
    },
    "top_server_error_key_report": {
        "500": [
            {
                "type_req": "POST",
                "url": "/administrator/index.php",
                "status": 500,
                "ip": "188.123.230.195"
            },
            {
                "type_req": "POST",
                "url": "/administrator/index.php",
                "status": 500,
                "ip": "188.123.230.195"
            },
            {
                "type_req": "POST",
                "url": "/administrator/index.php",
                "status": 500,
                "ip": "188.123.230.195"
            },
            {
                "type_req": "POST",
                "url": "/administrator/index.php",
                "status": 500,
                "ip": "188.123.230.195"
            },
            {
                "type_req": "POST",
                "url": "/administrator/index.php",
                "status": 500,
                "ip": "188.123.230.197"
            },
            {
                "type_req": "POST",
                "url": "/administrator/index.php",
                "status": 500,
                "ip": "188.123.230.196"
            },
            {
                "type_req": "POST",
                "url": "/administrator/index.php",
                "status": 500,
                "ip": "188.123.230.196"
            }
        ],
        "501": [
            {
                "type_req": "Head",
                "url": "//images/stories/movie.php",
                "status": 501,
                "ip": "113.161.24.118"
            }
        ],
        "502": [
            {
                "type_req": "POST",
                "url": "/administrator/index.php",
                "status": 502,
                "ip": "188.123.230.196"
            }
        ],
        "504": [
            {
                "type_req": "POST",
                "url": "/administrator/index.php",
                "status": 504,
                "ip": "188.123.230.196"
            }
        ],
        "524": [
            {
                "type_req": "POST",
                "url": "/administrator/index.php",
                "status": 524,
                "ip": "188.123.230.196"
            }
        ]
    }
}
```