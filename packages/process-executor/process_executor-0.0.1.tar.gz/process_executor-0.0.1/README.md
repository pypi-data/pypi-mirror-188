# Python Process Ececutor

Эта микросервис запускающий bash скрипты.\
Скрипты беруться только из Git.\
Скрипты выполняются в своем виртуальном окружении.

Пример конфига для процесса
```
{
  "workplan_id": "821e40ee-d3c9-41da-85d2-d12d5183998a",
  "name": "1",
  "command": [
    "{executable}", "./scripts/yandex_direct_export_to_file.py", "--body_filepath", "./scripts/body-clients.json", "--filepath", "clients.tsv", "--resource", "clients", "--token", ""
  ],
  "git": {
    "url": "https://github.com/pavelmaksimov/tapi-yandex-direct"
  },
  "venv": {
    "version": "3.7",
    "requirements": [
      "tapi_yandex_direct"
    ]
  },
  "time_limit": 100,
  "expires_utc": "2023-01-16T15:15:54.818Z",
  "save_stdout": false,
  "save_stderr": true
}
```




## Run
Set environment variable `PROCESS_EXECUTOR_HOME`

    process_executor --help
    process_executor