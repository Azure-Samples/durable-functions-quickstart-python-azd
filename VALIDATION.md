# Validation Notes

## Sample Structure
This Python Durable Functions quickstart sample has been created based on the .NET reference sample from:
https://github.com/Azure-Samples/durable-functions-quickstart-dotnet-azd

## Key Components

### Source Code (/src)
- **function_app.py**: Contains the main durable functions application with:
  - HTTP trigger (`http_start`) to start orchestrations
  - Orchestrator function (`FetchOrchestration`) that implements fan-out/fan-in pattern
  - Activity function (`fetch_title`) that fetches article titles from URLs
- **host.json**: Configured with extension bundle v4.x for Durable Functions
- **requirements.txt**: Python dependencies (azure-functions, azure-functions-durable, aiohttp)

### Infrastructure (/infra)
- **main.bicep**: Main infrastructure template configured for Python 3.12 runtime
- **app/api.bicep**: Function App configuration for Flex Consumption plan
- **app/rbac.bicep**: Role-based access control assignments
- **app/vnet.bicep**: Virtual network configuration (optional)
- **app/storage-PrivateEndpoint.bicep**: Private endpoint for storage (when VNet enabled)

### Configuration
- **azure.yaml**: Azure Developer CLI configuration pointing to Python project
- **.vscode/**: VS Code settings for Python development
- **.devcontainer/**: Codespaces/Dev Container configuration

## Local Testing Requirements
To test locally:
1. Python 3.12
2. Azure Functions Core Tools v4
3. Azurite (storage emulator)
4. Virtual environment with dependencies from requirements.txt

## Deployment Requirements
- Azure subscription
- Azure Developer CLI (azd)
- Region that supports Flex Consumption plan

## Differences from .NET Sample
- Runtime changed from dotnet-isolated 8.0 to Python 3.12
- Project structure uses /src instead of /fanoutfanin
- Uses Python v2 programming model with decorators
- Different dependency management (requirements.txt vs .csproj)
- VS Code configuration adapted for Python debugging

## Best Practices Applied
- Uses Azure Verified Modules (AVM) in bicep
- Managed identity for authentication (no connection strings)
- Optional VNet for enhanced security
- Extension bundle v4.x (latest stable)
- Python 3.12 (latest stable version)
