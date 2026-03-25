#!/bin/bash
set -euo pipefail

# ── Usage ─────────────────────────────────────────────────────────────────────

usage() {
  echo "Usage: $0 --env <dev|prod> --location <azure-region>"
  echo "  Example: $0 --env dev --location eastus"
  exit 1
}

# ── Parse arguments ────────────────────────────────────────────────────────────

ENV=""
LOCATION=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env)      ENV="$2";      shift 2 ;;
    --location) LOCATION="$2"; shift 2 ;;
    *) usage ;;
  esac
done

[[ -z "$ENV" || -z "$LOCATION" ]] && usage
[[ "$ENV" != "dev" && "$ENV" != "prod" ]] && { echo "Error: --env must be 'dev' or 'prod'"; exit 1; }

# ── Check prerequisites ────────────────────────────────────────────────────────

for cmd in az func openssl; do
  command -v "$cmd" &>/dev/null || { echo "Error: '$cmd' is not installed."; exit 1; }
done

az account show &>/dev/null || { echo "Error: not logged in to Azure. Run 'az login' first."; exit 1; }

# ── Config ────────────────────────────────────────────────────────────────────

RESOURCE_GROUP="rg-br-${ENV}-${LOCATION}"
FUNC_APP="func-br-${ENV}-${LOCATION}"
NTFY_TOPIC="br-$(openssl rand -hex 8)"
TAGS="Environment=${ENV} Project=birthday-reminder"

echo ""
echo "Deploying birthday-reminder"
echo "  Environment:    ${ENV}"
echo "  Location:       ${LOCATION}"
echo "  Resource group: ${RESOURCE_GROUP}"
echo "  Function app:   ${FUNC_APP}"
echo "  ntfy topic:     ${NTFY_TOPIC}"
echo ""

# ── Resource group ─────────────────────────────────────────────────────────────

echo "==> Creating resource group..."
az group create \
  --name "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --tags $TAGS \
  --output none

# ── Infrastructure ─────────────────────────────────────────────────────────────

echo "==> Deploying infrastructure..."
az deployment group create \
  --resource-group "$RESOURCE_GROUP" \
  --template-file infra/main.bicep \
  --parameters env="$ENV" ntfyTopic="$NTFY_TOPIC" \
  --output none

# ── Wait for function app to be ready ─────────────────────────────────────────

echo "==> Waiting for function app to be ready..."
sleep 30

# ── Function code ──────────────────────────────────────────────────────────────

echo "==> Publishing function code..."
func azure functionapp publish "$FUNC_APP"

# ── Web app .env ───────────────────────────────────────────────────────────────

echo "==> Writing web/.env..."
STORAGE_ACCOUNT=$(az deployment group show \
  --resource-group "$RESOURCE_GROUP" --name "main" \
  --query "properties.outputs.storageAccountName.value" -o tsv)
CONN_STRING=$(az storage account show-connection-string \
  --name "$STORAGE_ACCOUNT" --resource-group "$RESOURCE_GROUP" \
  --query "connectionString" -o tsv)

cat > web/.env <<EOF
STORAGE_CONNECTION_STRING=${CONN_STRING}
EOF

# ── Save ntfy topic ────────────────────────────────────────────────────────────

echo "$ENV $NTFY_TOPIC\n" >> .ntfy_topic.tmp

echo ""
echo "Done! Subscribe to your ntfy topic to receive birthday notifications:"
echo "  https://ntfy.sh/${NTFY_TOPIC}"
