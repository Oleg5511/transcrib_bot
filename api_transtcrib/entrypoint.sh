#!/bin/bash
cd src
alembic upgrade head
python cli.py admin@admin.com password
python main.py