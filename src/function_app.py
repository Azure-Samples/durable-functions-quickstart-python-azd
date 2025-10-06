import logging
import re
import azure.functions as func
import azure.durable_functions as df
from aiohttp import ClientSession

myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@myApp.route(route="FetchOrchestration_HttpStart")
@myApp.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    """HTTP trigger to start the orchestration."""
    instance_id = await client.start_new("FetchOrchestration")
    
    logging.info(f"Started orchestration with ID = '{instance_id}'.")
    
    return client.create_check_status_response(req, instance_id)


@myApp.orchestration_trigger(context_name="context")
def fetch_orchestration(context: df.DurableOrchestrationContext):
    """Orchestrator function that fans out to fetch article titles in parallel."""
    logger = logging.getLogger("FetchOrchestration")
    logger.info("Fetching data.")
    
    # List of URLs to fetch titles from
    urls = [
        "https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-overview",
        "https://learn.microsoft.com/azure/azure-functions/durable/durable-task-scheduler/durable-task-scheduler",
        "https://learn.microsoft.com/azure/azure-functions/functions-scenarios",
        "https://learn.microsoft.com/azure/azure-functions/functions-create-ai-enabled-apps",
    ]
    
    # Run fetching tasks in parallel
    tasks = []
    for url in urls:
        task = context.call_activity("fetch_title", url)
        tasks.append(task)
    
    # Wait for all the parallel tasks to complete before continuing
    results = yield context.task_all(tasks)
    
    # Return fetched titles as a formatted string
    return "; ".join(results)


@myApp.activity_trigger(input_name="url")
async def fetch_title(url: str):
    """Activity function that fetches the title from a URL."""
    logger = logging.getLogger("FetchTitle")
    logger.info(f"Fetching from url {url}.")
    
    try:
        async with ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                content = await response.text()
                
                # Extract page title
                title_match = re.search(
                    r'<title[^>]*>([^<]+?)\s*\|\s*Microsoft Learn</title>',
                    content,
                    re.IGNORECASE
                )
                
                if title_match:
                    title = title_match.group(1).strip()
                else:
                    title = "No title found"
                
                return title
    except Exception as ex:
        return f"Error fetching from {url}: {str(ex)}"
