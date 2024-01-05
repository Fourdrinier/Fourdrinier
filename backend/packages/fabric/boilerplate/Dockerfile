FROM openjdk:${JAVA_VERSION}
WORKDIR /minecraft

# Download the latest version of Fabric for Minecraft version ${GAME_VERSION}
ADD "${LOADER_URL}" /minecraft/fabric.jar

# Download the Fabric API mod, as it is required for most Fabric mods
ADD "${FABRIC_API_URL}" /minecraft/mods/

# Download specified mods
${MOD_DOWNLOADS}

# Download mods listed as required dependencies of specified mods
${REQUIRED_DEPENDENCY_DOWNLOADS}

# Download mods listed as optional dependencies of specified mods
${OPTIONAL_DEPENDENCY_DOWNLOADS}

# Accept Minecraft's EULA
RUN echo 'eula=${EULA}' > /minecraft/eula.txt

# Expose the server's port
EXPOSE ${PORT}

# Start the Minecraft server
ARG ALLOCATED_MEMORY='1024M'
CMD java -Xmx${ALLOCATED_RAM} -jar /minecraft/fabric.jar nogui