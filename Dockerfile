FROM squidfunk/mkdocs-material:latest

# Set build directory
#WORKDIR /docs

# Copy files necessary for build
COPY ./ /docs

RUN \
  pip install --upgrade pip && \
  pip install -r /docs/requirements.txt

# Set working directory
WORKDIR /docs

# Expose MkDocs development server port
EXPOSE 8000

# Start development server by default
ENTRYPOINT ["mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000"]
