#########################################################
# Base
#########################################################
FROM node:22.10-alpine3.19 AS base

WORKDIR /app

#########################################################
# Debug
#########################################################
FROM base AS debug

EXPOSE 3000

CMD npm run dev

#########################################################
# Builder
#########################################################
FROM base AS builder

# Install dependencies
COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install --force

# Copy source code
COPY . .

# Build the app
RUN npm run build


#########################################################
# Production
#########################################################
FROM builder AS prod

EXPOSE 3000

CMD npm run start


