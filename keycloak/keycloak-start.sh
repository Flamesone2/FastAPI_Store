#!/bin/bash

minikube start

kubectl apply -f postgres-pvc.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f keycloak-deployment.yaml

echo "Waiting for pods to be ready..."
kubectl wait --for=condition=Ready pod -l app=postgres --timeout=300s
kubectl wait --for=condition=Ready pod -l app=keycloak --timeout=300s

echo "Keycloak URL:"
minikube service keycloak --url --https=false