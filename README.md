# WebStatusTracker

## Автоматическая проверка сайта на определенные статусы с уведомлением в Telegram боте!

* Логгирование в папку программы (logs.log)

Настройки (При первом запуске settings.json создаться.):
``` 
{
    "page_urls": [
        "https://httpstat.us/200",
        "https://httpstat.us/400",
        "https://httpstat.us/404",
        "https://example.com"
    ], // Сайты которые надо проверять на статусы.
    "status": {
        "error_status": [
            404,
            400,
            300
        ], // Статусы которые выдают ошибку.
        "approved_status": [
            200
        ] // Статусы которые выдают работоспособность сайта.
    },
    "bot": {
        "admin_id": 1, // Айди юзера которому будут отсылаться сообщения.
        "error_status_send": true, // Отправлять данные о сайтах которые выдают error_status.
        "approved_status_send": true // Отправлять данные о сайтах которые выдают approved_status.
    }, // true - Да, false - нет
    "schedule_seconds": 60 // Задержка при которой будут проверятся сайты на доступность.
}
```

## Установка нужных пакетов: 
```
pip install -r requirements.txt
```

## .env
```
BOT_TOKEN=TOKEN // TOKEN заменить на ваш токен бота.
```

