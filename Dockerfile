FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock .python-version ./

# Install dependencies from lockfile (no dev deps, no project itself)
RUN uv sync --frozen --no-dev --no-install-project

# Copy only the ETL script
COPY python-scripts/get_data.py python-scripts/get_data.py

CMD ["uv", "run", "python", "python-scripts/get_data.py"]
