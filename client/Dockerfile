FROM oven/bun:latest AS deps

WORKDIR /app

COPY package.json .

RUN bun i

FROM oven/bun:latest AS build

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN bun run build

FROM nginx:1.27.4-alpine AS runner

COPY --from=build /app/build /etc/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]