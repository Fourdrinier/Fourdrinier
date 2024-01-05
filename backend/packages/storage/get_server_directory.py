import os


async def get_server_directory(server_id, host=False):
    if host:
        server_directory = os.path.join(
            os.environ.get("STORAGE_PATH"), "servers", server_id
        )
    else:
        server_directory = os.path.join("/", "storage", "servers", server_id)
    return server_directory
