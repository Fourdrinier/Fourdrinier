ARG JAVA_VERSION
FROM openjdk:${JAVA_VERSION}
WORKDIR /minecraft

# Download the requested version of Paper
ADD "https://meta.fabricmc.net/v2/versions/loader/1.20.4/0.15.3/0.11.2/server/jar" /minecraft/fabric.jar

# Accept Minecraft's EULA
RUN echo "eula=true" > /minecraft/eula.txt

# Expose the Minecraft server port
EXPOSE 25565

# Command to start the Minecraft server
ARG ALLOCATED_RAM
CMD echo ${ALLOCATED_RAM}
CMD java -Xmx${ALLOCATED_RAM} -jar /minecraft/fabric.jar nogui