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

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Command to start the Minecraft server
ARG ALLOCATED_RAM='1024M'
ENV ALLOCATED_RAM=${ALLOCATED_RAM}
ENTRYPOINT ["/bin/sh", "-c", "/entrypoint.sh \"$@\"", "--"]
CMD ["${ALLOCATED_RAM}"]
CMD java -Xmx${ALLOCATED_RAM} -jar /minecraft/fabric.jar nogui