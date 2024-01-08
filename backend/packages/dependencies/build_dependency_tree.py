async def get_mod_dependencies(latest_mod_versions):
    required_dependencies = []
    optional_dependencies = []

    for version_object in latest_mod_versions:
        version = version_object["version"]
        dependencies = version["dependencies"]
        for dependency in dependencies:
            match dependency["dependency_type"]:
                case "required":
                    if dependency["project_id"] not in required_dependencies:
                        required_dependencies.append(dependency["project_id"])
                case "optional":
                    if dependency["project_id"] not in optional_dependencies:
                        optional_dependencies.append(dependency["project_id"])

    return required_dependencies, optional_dependencies
