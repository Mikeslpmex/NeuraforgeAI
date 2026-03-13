#!/bin/bash
# Script de Puesta en Marcha: Workload Identity Federation para NeuraforgeAI

PROJECT_ID="TU_ID_DE_PROYECTO"
POOL_NAME="neuraforge-pool"
PROVIDER_NAME="neuraforge-provider"
SERVICE_ACCOUNT="tesorero-sa@${PROJECT_ID}.iam.gserviceaccount.com"

echo "[+] Configurando Workload Identity Federation en Google Cloud..."
gcloud config set project $PROJECT_ID

echo "[1/4] Habilitando APIs necesarias..."
gcloud services enable iamcredentials.googleapis.com

echo "[2/4] Creando el Pool de Identidad (neuraforge-pool)..."
gcloud iam workload-identity-pools create $POOL_NAME \
    --location="global" \
    --description="Pool para la automatización de NeuraforgeAI" \
    --display-name="Neuraforge AI Pool"

echo "[3/4] Creando el Proveedor OIDC..."
# Aquí asumo que podrías usar GitHub Actions, GitLab o tu propio emisor.
# Si usas GitHub, el issuer es https://token.actions.githubusercontent.com
gcloud iam workload-identity-pools providers create-oidc $PROVIDER_NAME \
    --location="global" \
    --workload-identity-pool=$POOL_NAME \
    --display-name="Neuraforge OIDC Provider" \
    --attribute-mapping="google.subject=assertion.sub" \
    --issuer-uri="https://token.actions.githubusercontent.com"

echo "[4/4] Otorgando permisos a la Cuenta de Servicio..."
# Permitir que el pool asuma la identidad de la service account de Tesorero Orion
WORKLOAD_IDENTITY_POOL_ID=$(gcloud iam workload-identity-pools describe $POOL_NAME --location="global" --format="value(name)")

gcloud iam service-accounts add-iam-policy-binding $SERVICE_ACCOUNT \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/*"

echo "[✓] Vinculación completada con éxito."
