# ---------- 1) Build Stage ----------
FROM ubuntu:22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

# Install node & npm
RUN apt update && \
    apt install -y curl build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt install -y nodejs && \
    npm install -g npm

# Create app directory
WORKDIR /app

# Copy package.json first (cache optimization)
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy all source code
COPY . .

# Build frontend (Vite)
RUN npm run build


# ---------- 2) Runtime Stage ----------
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install nginx
RUN apt update && apt install -y nginx && apt clean

# Remove default nginx site
RUN rm -rf /var/www/html/*

# Copy built frontend from stage 1
COPY --from=builder /app/dist /var/www/html

# Expose port 80
EXPOSE 80

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
