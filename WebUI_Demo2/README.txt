# Build:

    docker build -t trading-ui-react .

# Run: Terminal 1 - Backend

    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Run: Terminal 2 - Frontend

    docker run -p 8080:80 trading-ui-react

# Access:

    http://localhost:8080