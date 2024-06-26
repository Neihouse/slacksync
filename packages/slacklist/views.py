from slack_bolt import View, Ack
from slack_sdk.models.blocks import Input, PlainTextObject, SectionBlock
from slack_sdk.web import WebClient
from .utils import save_list, get_list

# ----- Modal Views -----

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

# Add other modal views here as your toolkit grows
# For example: create_new_list_modal, create_edit_task_modal, etc.

# ----- Modal Submission Handlers -----

def handle_add_task_modal_submission(ack: Ack, body: dict, client: WebClient, logger):
    """Handles the submission of the add task modal."""
    ack()

    try:
        # Get Data (Improved Error Handling)
        list_name = body["view"].get("private_metadata")
        if not list_name:
            raise ValueError("List name not found in modal data.")

        task_description = body["view"]["state"]["values"]["task_description_block"]["task_description_input"]["value"]

        # Input Validation
        if len(task_description) < 3:  # Check for minimum length
            raise ValueError("Task description must be at least 3 characters long.")

        # Logic to Add Task
        current_list = get_list(list_name)
        if not current_list:
            raise ValueError(f"List '{list_name}' not found.")

        current_list["items"].append({"description": task_description, "completed": False})
        save_list(current_list)

        logger.info(f"Task '{task_description}' added to list '{list_name}' (User ID: {body['user']['id']})")  # Detailed logging
        client.chat_postMessage(
            channel=body["user"]["id"],
            text=f"✅ Task '{task_description}' added to list '{list_name}' successfully!"
        )
    
    except ValueError as e:  # Specific error handling for validation errors
        logger.error(f"Error adding task: {e} (Request body: {body})")  # Log error with request payload
        client.chat_postMessage(
            channel=body["user"]["id"],
            text=str(e)
        )
    except Exception as e:  # Catch any other unexpected errors
        logger.exception(f"Unexpected error adding task: {e} (Request body: {body})")  # Log full traceback with request payload
        client.chat_postMessage(
            channel=body["user"]["id"],
            text="❌ An unexpected error occurred while adding the task. Please try again later."
        )


# Add submission handlers for other modals here
# For example: handle_new_list_modal_submission, handle_edit_task_modal_submission, etc.