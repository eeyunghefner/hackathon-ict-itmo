# hackathon-ict-itmo

Приложение для организации и учета хакатонов в университете ИТМО. Система унифицирует процесс проведения хакатонов и подобных мероприятий в рамках учебного заведения.

## Запуск frontend

```bash
git clone <rep_name>
cd client/hackathon-ict-itmo
npm install
npm run dev
```

**Примечание:** Если возникает ошибка `npm command not found`, установите [Node.js](https://nodejs.org/).

## Запуск backend

1. Клонируйте репозиторий и перейдите в backend:
   ```bash
   git clone <repo-url>
   cd hackathon-ict-itmo/server
   ```

2. Создайте файл `app/.env` на основе `.env.example` и укажите следующие значения:
```
POSTGRES_USER=hackathon
POSTGRES_PASSWORD=123
POSTGRES_DB=hackathon
JWT_SECRET_KEY=dev-secret-key
JWT_EXPIRE_MINUTES=60
DATABASE_URL=postgresql+asyncpg://hackathon:123@hackathon-server-postgres:5432/hackathon
```

3. Поднимите PostgreSQL:
```bash
docker compose up -d db
```

4. Загрузите схему БД и тестовые данные **один раз**:
```bash
docker exec -i hackathon-server-postgres psql -U hackathon -d hackathon < init.sql
```

5. Поднимите backend:
```bash
docker compose up -d app
docker compose logs -f app
```

6. Проверьте работу API:
```bash
curl -i http://localhost:8000/docs
```

Если всё работает корректно, Swagger UI будет доступен по адресу [http://localhost:8000/docs](http://localhost:8000/docs).

Скринкаст приложения доступен по ссылке ниже:

https://drive.google.com/file/d/1wYae7CGaMr1ZZjrKqJHtZBjjV8kXVV00/view?usp=sharing 
