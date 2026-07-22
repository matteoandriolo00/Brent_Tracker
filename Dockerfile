FROM node:20-slim AS frontend-builder

WORKDIR /app-frontend

COPY brent-tracker-frontend/package.json brent-tracker-frontend/package-lock.json ./
RUN npm install

COPY brent-tracker-frontend/ ./
RUN npm run build

FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv
RUN uv sync --frozen --no-dev

COPY . .

COPY --from=frontend-builder /app-frontend/dist ./brent-tracker-frontend/dist

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]