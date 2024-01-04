ARG JAVA_VERSION
FROM openjdk:${JAVA_VERSION}
WORKDIR /minecraft

# Download the requested version of Paper
ARG LOADER_URL
ADD "${LOADER_URL}" /minecraft/fabric.jar

# Doenload the necessary vanilla .jar
ARG VANILLA_URL
# Accept Minecraft's EULA
ARG EULA
RUN echo 'eula=${EULA}' > /minecraft/eula.txt

# Expose the Minecraft server port
EXPOSE 25565

# Command to start the Minecraft server
ARG ALLOCATED_RAM='1024M'
CMD java -Xmx${ALLOCATED_RAM} -jar /minecraft/fabric.jar nogui