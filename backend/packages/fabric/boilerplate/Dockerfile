FROM openjdk:${JAVA_VERSION}
WORKDIR /minecraft

# Download the latest version of Fabric for Minecraft version ${GAME_VERSION}
ADD "${LOADER_URL}" /minecraft/fabric.jar

# Accept Minecraft's EULA
RUN echo 'eula=${EULA}' > /minecraft/eula.txt

# Expose the server's port
EXPOSE ${PORT}

# Start the Minecraft server
ARG ALLOCATED_MEMORY='1024M'
CMD java -Xmx${ALLOCATED_RAM} -jar /minecraft/fabric.jar nogui