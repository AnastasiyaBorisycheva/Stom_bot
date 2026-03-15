## **3. Структура базы (SQLite)**

### **Таблица `users`**
Хранит информацию о пользователях (один раз при первом входе).

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER UNIQUE,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    source TEXT,                -- откуда пришёл (place param)
    first_seen DATETIME,
    last_seen DATETIME
);
```

### **Таблица `states`**
Хранит текущее состояние пользователя (FSM).

```sql
CREATE TABLE states (
    user_id INTEGER PRIMARY KEY,
    current_state TEXT,          -- например, 'bite_test_q1'
    data TEXT,                   -- JSON с дополнительными данными
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(tg_id)
);
```

### **Таблица `contacts`**
Хранит собранные контакты (телефон, почта).

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    phone TEXT,
    email TEXT,
    collected_at DATETIME,
    source_step TEXT,            -- на каком шаге собрали
    FOREIGN KEY (user_id) REFERENCES users(tg_id)
);
```

### **Таблица `events`**
Логирование ключевых событий (для аналитики воронки).

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_name TEXT,             -- 'start', 'problem_selected', 'test_passed', 'appointment_clicked'
    event_data TEXT,             -- JSON (например, какая проблема)
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(tg_id)
);
```