#development
FROM node:20-alpine
WORKDIR /app

#Install dependencies first to avoid rebuilding the cache
COPY package*.json ./
# Clean cache and install depednencies with specific version
RUN yarn cache clean && yarn install --frozen-lockfile

#Copy the source code and expose on dev port
COPY . .
EXPOSE 5173

CMD ["yarn", "dev", "--host", "0.0.0.0"]


