#########################################################
# Base
#########################################################
FROM node:22.10-alpine3.19 AS base

WORKDIR /app

# Install dependencies
COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install

# Copy source code
COPY . .

# Build the app
RUN npm run build

#########################################################
# Debug
#########################################################
FROM base AS debug

EXPOSE 3000

CMD npm run dev

#########################################################
# Production
#########################################################
FROM nginx:1.27.2-alpine-slim AS prod

EXPOSE 3000

WORKDIR /app
COPY --from=base /app/out /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf


