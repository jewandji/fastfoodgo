FROM python:3.10-slim

WORKDIR /app

# On copie TOUT ce qui est nécessaire (config + code)
COPY pyproject.toml README.md ./
COPY src/ src/

# ENSUITE on installe le paquet.
# Maintenant que 'src/' est là, pip va bien trouver le code fastfoodgo.
RUN pip install --no-cache-dir .

CMD ["python"]