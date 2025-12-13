import os
import time
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql+asyncpg://admin:admin123@database:5432/staycation')
# sqlalchemy sync driver url
sync_url = DATABASE_URL.replace('+asyncpg', '')

retries = 20
for i in range(retries):
    try:
        engine = create_engine(sync_url)
        conn = engine.connect()
        conn.close()
        print('database available')
        break
    except Exception as e:
        print('waiting for database, retry', i + 1, 'of', retries, '-', str(e))
        time.sleep(2)
else:
    raise SystemExit('Database not available after retries')
