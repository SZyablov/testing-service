# Сервис тестирования

[![Docker Image CI](https://github.com/SZyablov/testing-service/actions/workflows/docker-image.yml/badge.svg)](https://github.com/SZyablov/testing-service/actions/workflows/docker-image.yml)

## Техническое задание
<details><summary>Подробнее</summary>

### Основная информация
Необходимо разработать сервис тестирования. Имеются наборы тестов с вариантами ответов, один или несколько вариантов должны быть правильными

### Функциональные части сервиса
* Регистрация пользователя
* Аутентификация пользователя
* Зарегистрированные пользователи могут:
  * Пройти любой из наборов тестов
  * Последовательно отвечать на все вопросы, каждый вопрос должен отображаться на новой странице с отправкой формы (повторный ответ и оставление вопроса без ответа не допускается)
  * После прохождения теста вы можете увидеть результат:
    * количество правильных/неправильных ответов
    * процент правильных ответов

### Разделы панели администратора
* Стандартный раздел пользователя
* Раздел с наборами тестов
* Возможность:
  * добавлять вопросы
  * добавлять ответы на вопросы
  * отмечать правильные ответы
* Проверка того, что должен быть хотя бы 1 правильный вариант
* Проверка того, что все варианты не могут быть правильными
* Удаление вопросов/ответов/изменение правильных решений при редактировании тестовых наборов

### Требования
* Список всех зависимостей должен храниться в `requirements.txt` для возможности их установки с помощью `pip install -r requirements.txt`
* Разработка должна вестись в `.venv`, но сам каталог `.venv` должен быть добавлен в `.gitignore`
* Настройки должны храниться в `settings.py`, но если в той же директории есть `settings_local.py`, настройки из `settings_local.py` должны переопределять настройки в `settings.py`. Если существует файл `settings_local.py`, то настройки, определенные в нем, имеют более высокий приоритет. Сам файл `settings_local.py` добавляется в `.gitignore`. Таким образом, каждый разработчик и бета-сервер может использовать собственные настройки
</details>

## Технологии

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-v5.0.7-blue?logo=Django)](https://www.djangoproject.com/)
[![SQLite3](https://img.shields.io/badge/-SQLite3-464646?logo=SQLite)](https://www.sqlite.com/version3.html)
[![docker_compose](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)

## Установка

### Необходимые условия
* [Docker](https://www.docker.com/products/docker-desktop/) установлен в вашей системе
* Git установлен

### Шаг 1: Клонирование репозитория

1) Откройте терминал (Command Prompt, PowerShell или Git Bash).

2) Перейдите в каталог, в который вы хотите клонировать проект:
```
cd /path/to/your/directory
```
или для Windows:
```
cd "C:\Path\To\Your\Directory"
```

3) Клонируйте репозиторий с помощью Git
```
git clone https://github.com/SZyablov/testing-service.git
```

4) Переместитесь в каталог проекта
```
cd <имя директории проекта>
```

### Шаг 2: Сборка и запуск контейнеров docker

1) Убедитесь, что проект содержит файлы `Dockerfile` и `docker-compose.yml`. Эти файлы определяют, как будет собираться и запускаться контейнер Docker
2) Соберите контейнер Docker с помощью Docker Compose
```
docker-compose build
```
и запустите его
```
docker-compose up -d
```

Отладочные наборы тестов будут созданы автоматически. Служба тестирования будет работать на порту 8000

### Шаг 3: Создание суперпользователя

1) Просмотрите запущенные контейнеры
```
docker-compose ps
```
2) Посмотрите колонку SERVICE в строке контейнеров, чтобы использовать ее в команде для создания суперпользователя
```
docker-compose exec -ti <service-name> python3 testing/manage.py createsuperuser
```
3) Следуйте подсказкам, чтобы задать имя пользователя, электронную почту и пароль для суперпользователя проекта

## Использование

### Для пользователя

1) Откройте http://127.0.0.1:8000/sign-up/ и зарегистрируйтесь.
2) Вы будете перенаправлены на страницу входа в систему. Войдите в систему, указав имя пользователя и пароль
3) Выберите любой набор тестов
4) Ответьте на вопросы
5) После того как вы ответите на все вопросы, вы получите окно с результатами
6) Вы можете выйти из системы, воспользовавшись ссылкой "Выход".

Вы можете оставить вопросы без ответа и продолжить тест с того места, на котором остановились

### Для администратора

1) Откройте http://127.0.0.1:8000/admin/ и войдите в систему с учетными данными суперпользователя.
2) Откройте таблицу "Наборы тестов" и нажмите "Добавить набор тестов" (или просто нажмите "+ Add")
    1) Введите название и описание тестового набора
    2) Нажмите "Сохранить"
    3) Вы можете добавить вопросы перед сохранением, нажав "Добавить еще один вопрос" и введя вопрос в соответствующее поле
3) Откройте таблицу "Вопросы" и нажмите "Добавить вопрос" (или просто нажмите "+ Добавить")
    1) Выберите набор тестов для вопроса
    2) Введите текст вопроса
    3) Добавьте ответы и укажите, правильные они или нет, нажав "Добавить другой ответ" и установив соответствующие флажки.

Вы также можете редактировать ранее созданные наборы тестов, вопросы и ответы

## Возможные ошибки

### Bind for 0.0.0.0:8000 failed: port is already allocated
Данная ошибка означает, что порт 8000 уже занят. Для исправления ошибки откройте `docker-compose.yml` и в строке `port` измените значение на любое другое
