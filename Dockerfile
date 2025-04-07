# ----------- Frontend Build Stage -----------
FROM node:18 AS build-stage

WORKDIR /app

COPY package*.json tsconfig.json webpack.config.js ./
COPY static/ static/

RUN npm install
RUN npm run build


# ----------- Backend Stage -----------
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	&& rm -rf /var/lib/apt/lists/*

COPY . .

COPY --from=build-stage /app/static/dist ./static/dist

RUN pip install --no-cache-dir -r requirements-prod.txt

EXPOSE 5000

CMD ["python", "entrypoint.py"]
