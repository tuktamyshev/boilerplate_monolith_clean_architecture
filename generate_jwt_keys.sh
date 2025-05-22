#!/bin/bash

# Create directory for keys if it doesn't exist
mkdir -p certs

# Generate private key (RSA 2048 bits)
openssl genrsa -out certs/jwt_private.pem 2048

# Generate public key from private key
openssl rsa -in certs/jwt_private.pem -pubout -out certs/jwt_public.pem

# Set proper permissions
chmod 600 certs/jwt_private.pem
chmod 644 certs/jwt_public.pem

echo "JWT keys generated in keys directory:"
echo "- certs/jwt_private.pem - Private key for signing tokens"
echo "- certs/jwt_public.pem - Public key for verifying tokens"