# Use official lightweight Node.js image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency definition files first for optimal Docker layer caching
COPY package*.json ./

# Install npm dependencies
RUN npm install

# Copy frontend application code
COPY . .

# Expose Vite/React development server port
EXPOSE 5173

# Run development server exposed to host network
CMD ["npm", "run", "dev", "--", "--host"]