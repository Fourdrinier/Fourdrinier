FROM openjdk:${JAVA_VERSION}
WORKDIR /minecraft

# Download the latest version of ${LOADER} for Minecraft version ${GAME_VERSION}
ADD "${LOADER_URL}" /minecraft/server.jar


# Download specified mods
${MOD_DOWNLOADS}

# Download mods listed as required dependencies of specified mods
${REQUIRED_DEPENDENCY_DOWNLOADS}

# Download mods listed as optional dependencies of specified mods

# Accept Minecraft's EULA
RUN echo 'eula=${EULA}' > /minecraft/eula.txt

# Add properties to server.properties
RUN echo -e ${SERVER_PROPERTIES} > /minecraft/server.properties

# Add ops to ops.json
RUN echo ${OPS} > /minecraft/ops.json

# Expose the server's port
EXPOSE 25565

# Copy the entrypoint.txt script into the container
COPY entrypoint.txt /entrypoint.sh

# Ensure the entrypoint script is Unix-compatible (git will tailor it upon clone)
RUN sed -i 's/\r$//' /entrypoint.sh

# Make the entrypoint.txt script executable
RUN chmod +x /entrypoint.sh

# Command to start the Minecraft server
ENTRYPOINT ["/bin/sh", "-c", "/entrypoint.sh \"$@\"", "--"]
CMD ["${ALLOCATED_RAM}"]