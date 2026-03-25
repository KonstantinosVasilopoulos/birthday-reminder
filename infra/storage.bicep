// Storage Account and Table for birthday data
// Naming: st + workload + env + location + unique suffix (no hyphens, max 24 chars)

@description('Azure region for all resources.')
param location string

@description('Environment abbreviation.')
@allowed(['dev', 'prod'])
param env string

@description('Resource tags.')
param tags object

var suffix = uniqueString(resourceGroup().id)
var storageAccountName = 'stbr${env}${location}${take(suffix, 4)}'
var tableName = 'birthdays'

// ── Storage Account ───────────────────────────────────────────────────────────

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  tags: tags
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

// ── Table Service + Table ─────────────────────────────────────────────────────

resource tableService 'Microsoft.Storage/storageAccounts/tableServices@2023-05-01' = {
  parent: storageAccount
  name: 'default'
}

resource birthdaysTable 'Microsoft.Storage/storageAccounts/tableServices/tables@2023-05-01' = {
  parent: tableService
  name: tableName
}

// ── Outputs ──────────────────────────────────────────────────────────────────

output storageAccountName string = storageAccount.name
output connectionString string = 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net'
