# Script-Master

Сервис, который по конфигам (формат YAML), 
создает задания запуска скриптов в сервисе [Process-Executor](https://github.com/pavelmaksimov/process-executor),
согласно плану запусков полученных от сервиса [Work-Planner](https://github.com/pavelmaksimov/work-planner).

## Install
    poetry add script-master

or

    pip install script-master

## Run
    script-master --help
    script-master init # Создаст конфиг в текущий директории
    script-master run # Пользоваться командой, запускать всегда в директории, в которой выполнен init

## Интерфейс
Есть [интерфейс](https://github.com/pavelmaksimov/script-master-helper), он не обязателен. Для сервиса требуются только конфиги yaml, их иожно вручную создавать
Запускается отдельно/