ARG JAVA_VERSION
FROM openjdk:${JAVA_VERSION}
WORKDIR /minecraft

# Download the requested version of Paper
ADD "https://api.papermc.io/v2/projects/paper/versions/1.16.5/builds/794/downloads/paper-1.16.5-794.jar" /minecraft/paper.jar

# Accept Minecraft's EULA, replace with your own logic if needed
RUN echo "eula=true" > /minecraft/eula.txt

# Expose the Minecraft server port
EXPOSE 25565

# Command to start the Minecraft server
CMD ["java", "-jar", "/minecraft/paper.jar"]

