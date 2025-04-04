##!/bin/bash

minikube start

kubectl apply -f postgres-pvc.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f keycloak-deployment.yaml

echo "Waiting for pods to be ready..."
kubectl wait --for=condition=Ready pod -l app=postgres --timeout=300s
kubectl wait --for=condition=Ready pod -l app=keycloak --timeout=300s

# Получаем URL Keycloak
KEYCLOAK_URL=$(minikube service keycloak --url --https=false)

echo "Waiting for Keycloak to be ready..."
while ! curl -s "$KEYCLOAK_URL/auth/realms/master" > /dev/null; do
    echo "Keycloak is not ready yet. Retrying in 10 seconds..."
    sleep 10
done

echo "Keycloak is ready!"
echo "Keycloak URL: $KEYCLOAK_URL"