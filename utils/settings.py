import os
import json
import copy

import logging
logs = logging.getLogger(__name__)

class settings:
    def __init__(self, settings_path : str = "settings.json"):
        self.settings_path = settings_path
        self.settings_json_result = None
        self.settings_json_result_ = None

        self.settings_dict_example = {
            "page_urls": [
            "https://httpstat.us/200",
            "https://httpstat.us/400",
            "https://httpstat.us/404",
            "https://example.com"
            ],
            "status": {
            "error_status": [404, 400, 300],
            "approved_status": [200]
            },
            "bot": {
                "admin_id": 1,
                "error_status_send": True, 
                "approved_status_send": True
                },
            "schedule_seconds": 60
        }
    
    def _verify_settings(self):

        logs.debug("Начала работы функции _verify_settings.")

        try:
            logs.debug(f"Попытка открыть файл {self.settings_path}.")
            with open(self.settings_path, "r") as file:
                settings_json_result = json.load(file)
            logs.debug(f"Открыл файл {self.settings_path}. {settings_json_result}")
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            settings_json_result = {}
        
        self.settings_json_result_ = copy.deepcopy(settings_json_result)

        for key, value in self.settings_dict_example.items():
            if key not in settings_json_result:
                logs.warning(f"Настройки {key} не было в настройках!")
                settings_json_result[key] = value
            else:
                if isinstance(value, dict) and isinstance(settings_json_result[key], dict):
                    for sub_key, sub_value in value.items():
                        if sub_key not in settings_json_result[key]:
                            logs.warning(f"Подключ {sub_key} отсутствует в настройке {key}, добавляю значение по умолчанию.")
                            settings_json_result[key][sub_key] = sub_value
                        elif not isinstance(settings_json_result[key][sub_key], type(sub_value)):
                            logs.warning(f"Тип подключа {sub_key} в {key} не совпадает, заменяю на значение по умолчанию.")
                            settings_json_result[key][sub_key] = sub_value
                else:
                    if not isinstance(settings_json_result[key], type(value)):
                        logs.warning(f"Тип ключа {key} не совпадает, заменяю на значение по умолчанию.")
                        settings_json_result[key] = value

        self.settings_json_result = settings_json_result
            
    def _load_settings(self):
        self._verify_settings()

        if self.settings_json_result != self.settings_json_result_:
            with open(self.settings_path, 'w+') as file:
                json.dump(self.settings_json_result, file, indent=4, ensure_ascii=False)
            logs.info(f"Json в папке был с ошибками, программа их исправила и сохранила новый json!")
            exit(1)
        return self.settings_json_result