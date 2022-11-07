from os import getenv

import uvicorn

if __name__ == "__main__":
    host = getenv("HOST", "0.0.0.0")
    debug_mode = True if getenv("DEBUG", False) == "True" else False
    port = int(getenv("PORT", 8000))
    reload_dirs = getenv("RELOAD_DIRS", "/app").split(' ')

    server_config = uvicorn.Config(
        app="main:app",
        host=host,
        port=port,
        reload=debug_mode,
        reload_dirs=reload_dirs,
    )
    server = uvicorn.Server(server_config)
    server.run()

