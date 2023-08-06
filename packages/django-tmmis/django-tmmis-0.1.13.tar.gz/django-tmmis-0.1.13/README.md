![Pypi version](https://img.shields.io/pypi/v/django-tmmis.svg)
![Python versions](https://img.shields.io/pypi/pyversions/django-tmmis)

### Настройка

```shell
python -m pip install django~=3.2.11 django-mssql-backend
django-admin startproject config
```

Добавляем подключение к БД МИС в файле `config/config/settings.py`:
```python
DATABASES = {
    'default': {
        ...
    },
    'tmmis'  : {
        'ENGINE'  : 'sql_server.pyodbc',
        'NAME'    : 'ИМЯ БД',
        'USER'    : 'sa',
        'PASSWORD': 'ПАРОЛЬ К БД',
        'HOST'    : 'АДРЕС СЕРВЕРА',
        'PORT'    : 1433,
        'OPTIONS' : {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}
```

### Интроспекция БД

Unix:
```shell script
python config/manage.py inspectdb --database=tmmis {table_name} > tmmis/models/{table_name}.py
```

Windows:
```shell script
 py .\config\manage.py inspectdb --database=tmmis {table_name} > .\tmmis\models\{table_name}.py
```
