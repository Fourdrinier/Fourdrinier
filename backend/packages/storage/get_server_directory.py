import os


async def get_server_directory(server_id):
    server_directory = os.path.join("/", "storage", "servers", server_id)
    return server_directory
