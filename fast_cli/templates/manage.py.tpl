import uvicorn
import sys
from {{ project_name }}.urls import app

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "runserver":
        host = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8000
        uvicorn.run("{{ project_name }}.urls:app", host=host, port=port, reload=True)
