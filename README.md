# Fourdrinier

## Author: Ethan Brown

* **Email:** [ewbrowntech@gmail.com](mailto:ewbrowntech@gmail.com)
* **GitHub:** [ewbrowntech](https://github.com/ewbrowntech)
* **Discord:** @fortuity

## Purpose:

Fourdrinier is a containerized web application that allows to create and manage Minecraft servers as Docker containers.
This approach yields several advantages:

1) Common configurations (settings, mods, plugins) can be easily applied across multiple servers at once
2) Installation and configuration of all software dependencies is done automatically in a containerized environment on
   a per-server basis. **No more messing around with Java installations.
   No more determining which mods you have to install to use another**
3) Automatic update-checking for all software involved
4) Server management via an easy-to-use interface in a browser
5) Granular programmatic control via an intuitive API

## Installation:

Until proper continuous deployment is set up, you must clone the repository and launch it via Docker Desktop

### Step 1: Ensure you have Docker installed

### Step 2: Ensure you have Git installed

### Step 3: Clone the repository

        git clone https://github.com/Fourdrinier/Fourdrinier.git

### Step 4: Define a storage path in a .env file

A **.env** file tells Docker what environment variables to load into Fourdrinier when it is composed. In this case,
we will set a variable called "STORAGE_PATH" which points to the directory/folder in which we would like to store
our servers.

1) Pick a directory for storing servers
2) Copy its path
3) Within the root folder of Fourdrinier, create a file called **".env"**
4) Within .env, write something like the following:

         STORAGE_PATH="C:\Minecraft"

## Starting Fourdrinier

1) Open a terminal within the root directory of Fourdrinier
2) Run the following:

        docker-compose up

## Stopping Fourdrinier

1) Open a terminal within the root directory of Fourdrinier
2) Run the following:

        docker-compose down -v

