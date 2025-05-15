using './main.bicep'

param environmentName = readEnvironmentVariable('AZURE_ENV_NAME', 'macaetemplate')
param AZURE_LOCATION = readEnvironmentVariable('AZURE_ENV_LOCATION', 'eastus2')
param azureOpenAILocation = readEnvironmentVariable('AZURE_OPENAI_LOCATION', 'eastus2')

