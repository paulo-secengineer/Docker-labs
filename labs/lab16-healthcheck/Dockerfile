FROM nginx:alpine

WORKDIR /usr/share/nginx/html

COPY index.html .

EXPOSE 80

HEALTHCHECK --interval=5s --timeout=3s --start-period=3s --retries=2 \
CMD wget --quiet --tries=1 --spider http://localhost:80/ || exit 1
