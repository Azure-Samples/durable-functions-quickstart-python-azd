<!--
---
name: Durable Functions Python Fan-Out/Fan-In (Durable Task Scheduler)
description: This repository contains a Durable Functions quickstart written in Python demonstrating the fan-out/fan-in pattern. It uses the Azure Durable Task Scheduler (DTS) backend and is deployed to Azure Functions Flex Consumption via the Azure Developer CLI (azd).
page_type: sample
products:
- azure-functions
- azure
- entra-id
urlFragment: starter-durable-fan-out-fan-in-python
languages:
- python
- bicep
- azdeveloper
---
-->

# Durable Functions Fan-Out/Fan-In quickstart - Python (Durable Task Scheduler backend)

This template repository contains a Durable Functions sample demonstrating the fan-out/fan-in pattern in Python (v2 programming model), backed by the **[Azure Durable Task Scheduler (DTS)][Azure Durable Task Scheduler]**. The sample can be easily deployed to Azure using the Azure Developer CLI (`azd`). It uses a user-assigned managed identity and can optionally deploy a virtual network.

[Durable Functions](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-overview) orchestrates stateful, long-running, multi-step logic with *durable execution*. State is persisted by a [backend provider](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-storage-providers). This sample uses the **[Azure Durable Task Scheduler]** provider, a fully managed backend purpose-built for Durable Functions and the Durable Task Framework. It replaces the Azure Storage backend and provides a dedicated dashboard for monitoring orchestrations.

> This sample uses the standard Functions extension bundle (`Microsoft.Azure.Functions.ExtensionBundle`, version `[4.*, 5.0.0)`), which provides the `azureManaged` storage provider for the Durable Task Scheduler backend.

## Prerequisites

+ [Python 3.11+](https://www.python.org/downloads/)
+ [Azure Functions Core Tools v4](https://learn.microsoft.com/azure/azure-functions/functions-run-local?pivots=programming-language-python#install-the-azure-functions-core-tools)
+ [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
+ [Azurite storage emulator](https://learn.microsoft.com/azure/storage/common/storage-use-azurite)
+ To run/debug in Visual Studio Code:
  + [Visual Studio Code](https://code.visualstudio.com/)
  + [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
  + [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

## Initialize the local project

You can initialize a project from this `azd` template in one of these ways:

+ Use `azd init` from an empty local folder:

    ```shell
    azd init --template durable-functions-quickstart-python-azd
    ```

+ Or clone directly:

    ```shell
    git clone https://github.com/Azure-Samples/durable-functions-quickstart-python-azd.git
    cd durable-functions-quickstart-python-azd
    ```

## Provision Azure resources

This sample uses a remote Durable Task Scheduler (DTS) resource in Azure as the Durable Functions backend.

> [!NOTE]
> As an alternative to connecting to a remote DTS resource during local development, you can instead use the [Durable Task Scheduler Emulator](https://learn.microsoft.com/azure/azure-functions/durable/durable-task-scheduler/durable-task-scheduler-emulator), which runs locally in a Docker container. The emulator provides a fully functional DTS instance without requiring Azure resources but does require Docker to be installed.

Run this command to provision the required Azure resources, including the DTS instance:

```shell
azd auth login
azd provision
```

You're prompted to supply these required deployment parameters:

| Parameter | Description |
| ---- | ---- |
| _Environment name_ | An environment that's used to maintain a unique deployment context for your app. You won't be prompted if you created the local project using `azd init`.|
| _Azure subscription_ | Subscription in which your resources are created.|
| _Azure location_ | Azure region in which to create the resource group that contains the new Azure resources. Only regions that currently support the Flex Consumption plan are shown.|
| _vnetEnabled_ | Whether to deploy with a virtual network for enhanced security. Select `true` or `false`.|

After provisioning completes, a `postprovision` hook automatically generates the `src/local.settings.json` file with your DTS connection information.

### Create and activate a virtual environment

In the `src` folder, create and activate a virtual environment named `.venv`:

**Linux/macOS:**

```bash
cd src
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

```cmd
cd src
py -m venv .venv
.venv\scripts\activate
```

### Install dependencies

From the `src` folder with the virtual environment activated, run this command to install the required dependencies:

```console
pip install -r requirements.txt
```

## Run your app from the terminal

1. Start the Azurite storage emulator. The Functions runtime requires a storage component for internal state management:

    ```shell
    azurite
    ```

1. In a separate terminal, navigate to the `src` folder with the virtual environment activated, and start the Functions host:

    ```shell
    func start
    ```

    You should see output similar to:

    ```shell
    Functions:

            http_start:  http://localhost:7071/api/orchestrators/{functionName}

            fetch_orchestration: orchestrationTrigger

            fetch_title: activityTrigger
    ```

1. In another terminal (or your browser), hit the HTTP trigger:
   <http://localhost:7071/api/orchestrators/fetch_orchestration>

    The HTTP endpoint returns a set of URLs that manage the orchestration, which looks like this fragment:

    ```json
    {
        "id": "9addc67238604701a38d1470874a5f04",
        "statusQueryGetUri": "http://localhost:7071/runtime/webhooks/durabletask/instances/9addc67238604701a38d1470874a5f04?taskHub=TestHubName&connection=Storage&code=<code>",
        "sendEventPostUri": "http://localhost:7071/runtime/webhooks/durabletask/instances/9addc67238604701a38d1470874a5f04/raiseEvent/{eventName}?taskHub=TestHubName&connection=Storage&code=<code>",
        "terminatePostUri": "http://localhost:7071/runtime/webhooks/durabletask/instances/9addc67238604701a38d1470874a5f04/terminate?reason={text}&taskHub=TestHubName&connection=Storage&code<code>"
    }
    ```

1. Navigate to the `statusQueryGetUri` URL in your browser to check the orchestration status. When the orchestration completes, the response looks like this:

    ```json
    {
        "name": "fetch_orchestration",
        "instanceId": "987adada388a496b85bbc5496a54dd58",
        "runtimeStatus": "Completed",
        "input": null,
        "output": "Durable Functions Overview: Stateful Serverless Workflows; Durable Task Scheduler - Durable Task; Azure Functions Scenarios; Use AI tools and models in Azure Functions",
        "createdTime": "2026-06-22T06:58:58Z",
        "lastUpdatedTime": "2026-06-22T06:59:00Z"
    }
    ```

    The `output` field contains the article titles fetched in parallel by the fan-out/fan-in orchestration.

1. Press Ctrl+C to stop the Functions host when finished.

## Run your app using Visual Studio Code

1. Open the repository folder in VS Code (`code .`).
1. Ensure Azurite is running, as described above.
1. Press **Run/Debug (F5)** to start the app in the debugger.
1. Trigger the orchestration with an HTTP request to <http://localhost:7071/api/orchestrators/fetch_orchestration>.

## Deploy to Azure

After you've verified the app works locally, deploy your code from the project root to the provisioned function app in Azure:

```shell
azd deploy
```

## Test deployed app

Once deployment is done, test the Durable Functions app by making an HTTP request to trigger the start of an orchestration. To get the function URL with access key, run the following: 

```shell
func azure functionapp list-functions "$(azd env get-value AZURE_FUNCTION_NAME)" --show-keys
```

Copy the `Invoke url` value for `http_start` and open it in a browser or use `curl` to start a new orchestration.

## Monitor with the DTS dashboard

In Azure, open the deployed Durable Task Scheduler resource (type `Microsoft.DurableTask/schedulers`) in the Azure portal and follow the **Dashboard** link to inspect orchestrations, activities, history, and instance state.

To find the scheduler name quickly:

```shell
azd show
```

## Redeploy your code

You can run the `azd deploy` command as many times as you need to deploy code updates to your function app. To reprovision infrastructure changes, run `azd provision` again.

>[!NOTE]
>Deployed code files are always overwritten by the latest deployment package.

## Clean up resources

```shell
azd down
```

## Troubleshooting

If you see the following transient error after `azd up`, rerun the command:

```
ERROR: error executing step command 'deploy --all': failed deploying service 'api': publishing zip file: deployment failed: [KuduSpecializer] Kudu has been restarted during deployment
```

[Azure Durable Task Scheduler]: https://learn.microsoft.com/azure/azure-functions/durable/durable-task-scheduler/durable-task-scheduler