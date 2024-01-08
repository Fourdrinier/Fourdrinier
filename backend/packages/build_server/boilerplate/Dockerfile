FROM openjdk:${JAVA_VERSION}
WORKDIR /minecraft

# Download the latest version of ${LOADER} for Minecraft version ${GAME_VERSION}
ADD "${LOADER_URL}" /minecraft/server.jar


# Download specified mods
${MOD_DOWNLOADS}

# Download mods listed as required dependencies of specified mods
${REQUIRED_DEPENDENCY_DOWNLOADS}

# Download mods listed as optional dependencies of specified mods
${OPTIONAL_DEPENDENCY_DOWNLOADS}

# Accept Minecraft's EULA
RUN echo 'eula=${EULA}' > /minecraft/eula.txt

# Expose the server's port
EXPOSE 25565

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Command to start the Minecraft server
ENTRYPOINT ["/bin/sh", "-c", "/entrypoint.sh \"$@\"", "--"]
CMD ["${ALLOCATED_RAM}"]