# Use an official Node.js image
FROM node:20

# Set the working directory inside the container
WORKDIR /app

# Copy package files first
#package.json
#package-lock.json

COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the React project
COPY . .

# Expose Vite's default port
EXPOSE 5173

# Start the development server
CMD ["npm", "run", "dev", "--", "--host"]