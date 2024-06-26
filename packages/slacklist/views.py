from slack_bolt import View, Ack
from slack_sdk.models.blocks import Input, PlainTextObject, SectionBlock
from slack_sdk.web import WebClient
from .utils import save_list, get_list

# Create Modal View for Adding Tasks
def create_add_task_modal(list_name):
    """Creates a modal view for adding a task to a list."""
    return View(
        type="modal",
        callback_id="add_task_modal",
        private_metadata=list_name,
        title=PlainTextObject(text=f"Add Task to {list_name}"),
        submit=PlainTextObject(text="Add"),
        close=PlainTextObject(text="Cancel"),
        blocks=[
            SectionBlock(
                text=PlainTextObject(text="Enter the task description:")
            ),
            Input(
                element=PlainTextObject(
                    type="plain_text_input", action_id="task_description"
                ),
                label=PlainTextObject(text="Task Description"),
            ),
        ],
    )

# Handle Modal Submission
def handle_add_task_modal_submission(ack: Ack, body: dict, client: WebClient, logger):
    """Handles the submission of the add task modal."""
    ack()
    
    # Get Data
    list_name = body["view"]["private_metadata"]
    task_description = body["view"]["state"]["values"]["task_description"]["task_description"]["value"]

    # Logic to Add Task
    try:
        current_list = get_list(list_name)
        if not current_list:
            raise ValueError(f"List '{list_name}' not found.")
        current_list["items"].append({"description": task_description, "completed": False})
        save_list(current_list)

        logger.info(f"Task '{task_description}' added to list '{list_name}'")
        client.chat_postMessage(
            channel=body["user"]["id"],
            text=f"✅ Task '{task_description}' added to list '{list_name}' successfully!"
        )
    except Exception as e:
        logger.error(f"Error adding task: {e}")
        client.chat_postMessage(
            channel=body["user"]["id"],
            text=f"❌ An error occurred while adding the task. Please try again later."
        )
