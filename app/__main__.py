import os
import uvicorn

if __name__ == "__main__":
    debug_mode = True if os.getenv("DEBUG", False) == "True" else False
    reload_dirs = os.getenv("RELOAD_DIRS", "/app").split(' ')

    server_config = uvicorn.Config(
        app="main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=debug_mode,
        reload_dirs=reload_dirs,
    )
    server = uvicorn.Server(server_config)
    server.run()
