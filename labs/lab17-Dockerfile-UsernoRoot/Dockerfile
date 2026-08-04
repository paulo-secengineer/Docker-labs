FROM python:3.10-slim

ARG BUILD_VERSION=1.0.0

ENV PORT=8080
ENV DEV_NAME="Mestre Supremo"

WORKDIR /app

RUN useradd -m appuser

COPY --chown=appuser:appuser app.py .

USER appuser

EXPOSE $PORT

HEALTHCHECK --interval=5s --timeout=3s --start-period=3s --retries=2 CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["python", "app.py"]
