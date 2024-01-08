import httpx


async def get_collection(collection_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.modrinth.com/v3/collection/{collection_id}"
        )
        if response.status_code == 404:
            raise CollectionNotFoundException(collection_id)
    collection = response.json()
    return collection


class CollectionNotFoundException(Exception):
    def __init__(self, project_id, collection_id):
        message = f"Collection ID {collection_id} not found."
        super().__init__(message)
