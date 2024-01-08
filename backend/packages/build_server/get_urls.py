async def get_version_urls(versions):
    version_urls = []
    for version in versions:
        version_urls.append(version["version"]["files"][0]["url"])
    return version_urls
