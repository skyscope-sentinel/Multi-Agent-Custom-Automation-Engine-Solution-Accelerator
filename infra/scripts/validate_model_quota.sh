#!/bin/bash

LOCATION=""
MODEL=""
DEPLOYMENT_TYPE="Standard"
CAPACITY=0

ALL_REGIONS=('australiaeast' 'eastus2' 'francecentral' 'japaneast' 'norwayeast' 'swedencentral' 'uksouth' 'westus')

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)
      MODEL="$2"
      shift 2
      ;;
    --capacity)
      CAPACITY="$2"
      shift 2
      ;;
    --deployment-type)
      DEPLOYMENT_TYPE="$2"
      shift 2
      ;;
    --location)
      LOCATION="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required params
MISSING_PARAMS=()
[[ -z "$LOCATION" ]] && MISSING_PARAMS+=("location")
[[ -z "$MODEL" ]] && MISSING_PARAMS+=("model")
[[ -z "$CAPACITY" ]] && MISSING_PARAMS+=("capacity")

if [[ ${#MISSING_PARAMS[@]} -ne 0 ]]; then
  echo "❌ ERROR: Missing required parameters: ${MISSING_PARAMS[*]}"
  echo "Usage: $0 --location <LOCATION> --model <MODEL> --capacity <CAPACITY> [--deployment-type <DEPLOYMENT_TYPE>]"
  exit 1
fi

if [[ "$DEPLOYMENT_TYPE" != "Standard" && "$DEPLOYMENT_TYPE" != "GlobalStandard" ]]; then
  echo "❌ ERROR: Invalid deployment type: $DEPLOYMENT_TYPE. Allowed values are 'Standard' or 'GlobalStandard'."
  exit 1
fi

MODEL_TYPE="OpenAI.$DEPLOYMENT_TYPE.$MODEL"

check_quota() {
  local region="$1"
  echo "🔍 Checking quota for $MODEL_TYPE in $region ..."

  MODEL_INFO=$(az cognitiveservices usage list --location "$region" --query "[?name.value=='$MODEL_TYPE']" --output json 2>/dev/null)

  if [[ -z "$MODEL_INFO" || "$MODEL_INFO" == "[]" ]]; then
    echo "⚠️  No quota info found for $MODEL_TYPE in $region"
    return 1
  fi

  CURRENT_VALUE=$(echo "$MODEL_INFO" | jq -r '.[0].currentValue // 0' | cut -d'.' -f1)
  LIMIT=$(echo "$MODEL_INFO" | jq -r '.[0].limit // 0' | cut -d'.' -f1)
  AVAILABLE=$((LIMIT - CURRENT_VALUE))

  echo "🔎 Model: $MODEL_TYPE | Used: $CURRENT_VALUE | Limit: $LIMIT | Available: $AVAILABLE"

  if (( AVAILABLE >= CAPACITY )); then
    echo "✅ Sufficient quota in $region"
    return 0
  else
    echo "❌ Insufficient quota in $region (Available: $AVAILABLE, Required: $CAPACITY)"
    return 1
  fi
}

# Try user-provided region
if check_quota "$LOCATION"; then
  exit 0
fi

# Try fallback regions
REMAINING_REGIONS=()
for region in "${ALL_REGIONS[@]}"; do
  if [[ "$region" != "$LOCATION" ]]; then
    REMAINING_REGIONS+=("$region")
  fi
done

echo "🔁 Trying fallback regions for available quota..."

for region in "${REMAINING_REGIONS[@]}"; do
  if check_quota "$region"; then
    echo "🚫 Deployment cannot proceed because the original region '$LOCATION' lacks sufficient quota."
    echo "➡️  You can retry using the available region: '$region'"
    echo "🔧 To proceed, update the 'AZURE_OPENAI_LOCATION' value in the 'main.bicepparam' file, then run:"
    echo "    azd env set AZURE_OPENAI_LOCATION '$region'"
    exit 1
  fi
done

echo "❌ ERROR: No available quota found in any of the fallback regions."
exit 1
