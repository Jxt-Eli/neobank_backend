import asyncio
from logging.config import fileConfig
import os

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# Base (MetaData) imports here
from models import Base  # ensure this import doesn't trigger app start side-effects

# load env (optional) and set DATABASE_URL into alembic config
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

config = context.config

# for alembic to pick up the URL from env
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# configure logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target metadata for 'alembic revision --autogenerate'
target_metadata = Base.metadata

def do_run_migrations(connection):
    """This runs inside connection.run_sync -> uses a synchronous API expected by alembic."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,      # detect column type changes
        # render_as_batch=True, # uncomment for SQLite alter-table support
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an async engine/connection."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # run_sync will call the synchronous `do_run_migrations` with a sync Connection
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (emit SQL strings)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
