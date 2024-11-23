# Используем базовый образ для nginx
FROM nginx:alpine

# Копируем файлы клиента в директорию, используемую nginx для статического контента
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY script.js /usr/share/nginx/html/

# Nginx автоматически запустится при старте контейнера