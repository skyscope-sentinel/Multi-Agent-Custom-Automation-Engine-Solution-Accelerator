param (
    [string]$Location,
    [string]$Model,
    [string]$DeploymentType = "Standard",
    [int]$Capacity
)

# Verify required parameters
$MissingParams = @()
if (-not $Location) { $MissingParams += "location" }
if (-not $Model) { $MissingParams += "model" }
if (-not $Capacity) { $MissingParams += "capacity" }
if (-not $DeploymentType) { $MissingParams += "deployment-type" }

if ($MissingParams.Count -gt 0) {
    Write-Error "❌ ERROR: Missing required parameters: $($MissingParams -join ', ')"
    Write-Host "Usage: .\validate_model_quota.ps1 -Location <LOCATION> -Model <MODEL> -Capacity <CAPACITY> [-DeploymentType <DEPLOYMENT_TYPE>]"
    exit 1
}

if ($DeploymentType -ne "Standard" -and $DeploymentType -ne "GlobalStandard") {
    Write-Error "❌ ERROR: Invalid deployment type: $DeploymentType. Allowed values are 'Standard' or 'GlobalStandard'."
    exit 1
}

$ModelType = "OpenAI.$DeploymentType.$Model"

function Check-Quota {
    param (
        [string]$Region
    )

    Write-Host "`n🔍 Checking quota for $ModelType in $Region ..."

    $ModelInfoRaw = az cognitiveservices usage list --location $Region --query "[?name.value=='$ModelType']" --output json
    $ModelInfo = $null

    try {
        $ModelInfo = $ModelInfoRaw | ConvertFrom-Json
    } catch {
        Write-Warning "⚠️ Failed to parse quota info for region: $Region"
        return $false
    }

    if (-not $ModelInfo) {
        Write-Host "⚠️ No quota information found for $ModelType in $Region"
        return $false
    }

    $CurrentValue = ($ModelInfo | Where-Object { $_.name.value -eq $ModelType }).currentValue
    $Limit = ($ModelInfo | Where-Object { $_.name.value -eq $ModelType }).limit

    $CurrentValue = [int]($CurrentValue -replace '\.0+$', '') # Remove decimals
    $Limit = [int]($Limit -replace '\.0+$', '') # Remove decimals

    $Available = $Limit - $CurrentValue
    Write-Host "🔎 Model: $ModelType | Used: $CurrentValue | Limit: $Limit | Available: $Available"

    if ($Available -ge $Capacity) {
        Write-Host "✅ Sufficient quota in $Region"
        return $true
    } else {
        Write-Host "❌ Insufficient quota in $Region (Available: $Available, Required: $Capacity)"
        return $false
    }
}

# List of fallback regions (excluding the one already tried)
$PreferredRegions = @('australiaeast', 'eastus2', 'francecentral', 'japaneast', 'norwayeast', 'swedencentral', 'uksouth', 'westus') | Where-Object { $_ -ne $Location }

# Try original location first
if (Check-Quota -Region $Location) {
    exit 0
}

Write-Host "`n🔁 Trying fallback regions for available quota..."

foreach ($region in $PreferredRegions) {
    if (Check-Quota -Region $region) {
        Write-Host "🚫 Deployment cannot proceed because the original region '$Location' lacks sufficient quota."
        Write-Host "➡️ You can retry using the available region: '$region'"
        Write-Host "🔧 To proceed, update the 'AZURE_OPENAI_LOCATION' value in the 'main.bicepparam' file, then run the following command:"
        Write-Host "    azd env set AZURE_OPENAI_LOCATION '$region'"

        # Optional: update `.azure/env` (uncomment if needed)
        # Add-Content ".azure/env" "`nAZURE_OPENAI_LOCATION=$region"

        # Exit with non-zero code to halt deployment
        exit 2
    }
}

Write-Error "❌ ERROR: No available quota found in any region."
exit 1
