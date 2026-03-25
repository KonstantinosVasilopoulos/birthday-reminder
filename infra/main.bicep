// Main entry point — wires together storage and function modules
// Deploy with: az deployment group create -g <rg> -f main.bicep

@description('Azure region for all resources.')
param location string = resourceGroup().location

@description('Environment abbreviation used in resource names.')
@allowed(['dev', 'prod'])
param env string = 'prod'

@description('ntfy topic to push birthday notifications to.')
param ntfyTopic string

@description('Number of days in advance to send an upcoming birthday reminder.')
param upcomingReminderDays int = 10

var tags = {
  Environment: env
  Project: 'birthday-reminder'
}

// ── Modules ──────────────────────────────────────────────────────────────────

module storage 'storage.bicep' = {
  name: 'storage'
  params: {
    location: location
    env: env
    tags: tags
  }
}

module function 'function.bicep' = {
  name: 'function'
  params: {
    location: location
    env: env
    tags: tags
    storageAccountName: storage.outputs.storageAccountName
    storageConnectionString: storage.outputs.connectionString
    ntfyTopic: ntfyTopic
    upcomingReminderDays: upcomingReminderDays
  }
}

// ── Outputs ──────────────────────────────────────────────────────────────────

output storageAccountName string = storage.outputs.storageAccountName
output functionAppName string = function.outputs.functionAppName
