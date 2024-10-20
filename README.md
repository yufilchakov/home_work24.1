Пример описания Dockerfile.

Этот проект использует Docker для создания контейнера с приложением на Python. В `Dockerfile` описаны все шаги,
необходимые для сборки и запуска приложения.

1. Базовый образ:
   ```dockerfile
   FROM python:3.12-slim

Используется минималистичный образ Python 3.12, который обеспечивает легковесную среду выполнения для приложения.

2. Установка рабочего каталога:
   WORKDIR /app

Устанавливает рабочий каталог для всех последующих команд. Все файлы и команды будут выполняться в каталоге /app.

3. Копирование файлов конфигурации:

COPY poetry.lock pyproject.toml ./

Копирует файлы poetry.lock и pyproject.toml в рабочий каталог. Эти файлы содержат информацию о зависимостях проекта.

4. Обновление pip:

RUN pip install --upgrade pip

Обновляет pip до последней версии для обеспечения совместимости с последними пакетами.

5. Установка Poetry:

RUN pip install poetry

Устанавливает Poetry — инструмент для управления зависимостями и упаковки Python-приложений.

6. Настройка Poetry:

RUN poetry config virtualenvs.create false

Настраивает Poetry так, чтобы он не создавал виртуальные окружения. Все зависимости будут установлены в глобальное
окружение контейнера.

7. Установка зависимостей:

RUN poetry install --no-root

Устанавливает все зависимости, указанные в pyproject.toml, без установки самого приложения (если оно является пакетом).

8. Копирование всех файлов проекта:

COPY . .

Копирует все файлы из текущего каталога в рабочий каталог контейнера (/app). Это включает в себя ваш код приложения и
другие необходимые файлы.

Пример описания docker-compose.yaml

Файл `docker-compose.yaml` определяет сервисы, необходимые для работы приложения, включая базу данных, кэш, основной
сервер приложения и задачи фоновой обработки. Ниже приведено описание каждого сервиса.

Описание сервисов
1.Redis:
redis:
image: redis:latest
restart: on-failure
expose:

- "6379"

Использует образ Redis последней версии.
Перезапускается в случае сбоя.
Открывает порт 6379 для внутреннего использования.

2.PostgreSQL:
db:
image: postgres:16-alpine
restart: on-failure
env_file:

- .env
  expose:
- "5432"
  volumes:
- pg_data:/var/lib/postgresql/data
  healthcheck:
  test: ["CMD-SHELL", "-c", "pg_isready -U $POSTGRES_USER"]
  interval: 10s
  retries: 5
  timeout: 5s

Использует образ PostgreSQL версии 16 на основе Alpine.
Перезапускается в случае сбоя.
Загружает переменные окружения из файла .env.
Открывает порт 5432 для внутреннего использования.
Использует том pg_data для хранения данных базы данных.
Настроен контроль состояния с помощью healthcheck.

3. Приложение:

app:
build: .
tty: true
ports:

- "8000:8000"
  command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
  depends_on:
  db:
  condition: service_healthy
  volumes:
- .:/app

Строится на основе текущего контекста (Dockerfile).
Открывает порт 8000 для доступа к приложению.
Выполняет миграции базы данных перед запуском сервера.
Зависит от сервиса базы данных, который должен быть в состоянии "здоровья".
Монтирует текущий каталог в контейнер.

4. Celery Worker:
   celery:
   build: .
   tty: true
   command: celery -A config worker -l INFO
   restart: on-failure
   volumes:
    - .:/app
      depends_on:
    - redis
    - db
    - app

Строится на основе текущего контекста (Dockerfile).
Запускает Celery Worker для обработки фоновых задач.
Перезапускается в случае сбоя.
Зависит от Redis, базы данных и основного приложения.

5. Celery Beat:
   celery-beat:
   build: .
   tty: true
   command: celery -A config beat -l INFO
   restart: on-failure
   volumes:
    - .:/app
      depends_on:
    - redis
    - db
    - app

Строится на основе текущего контекста (Dockerfile).
Запускает Celery Beat для планирования фоновых задач.
Перезапускается в случае сбоя.
Зависит от Redis, базы данных и основного приложения.

6. Объемы:

volumes:
pg_data:

Объем pg_data используется для хранения данных PostgreSQL. Это позволяет сохранять данные между перезапусками контейнера
и обеспечивает их постоянство.

Запуск приложения docker-compose up -d --build

