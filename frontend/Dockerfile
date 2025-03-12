# Base Node image
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Development image for debugging
FROM base AS debug
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Expose port
EXPOSE 3000

# Start Next.js in development mode
CMD ["npm", "run", "dev"]

# Build the application for production
FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build the Next.js application
RUN npm run build

# Production image
FROM base AS prod
WORKDIR /app

ENV NODE_ENV production

# Create public directory
RUN mkdir -p ./public

# Copy necessary files from the builder stage
# COPY --from=builder /app/public/ ./public/ 2>/dev/null || true
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Expose port
EXPOSE 3000

# Set the command to start the Next.js application
CMD ["node", "server.js"]
