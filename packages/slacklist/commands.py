from slack_bolt import Ack, Respond
from slack_sdk import WebClient
from .utils import create_list, save_list, get_list, add_task, mark_task_complete, delete_list

def register_commands(app):
    """Registers all slash commands with the Slack app."""
    
    # ---------------- Slacklist Commands ----------------

    # Create List
    @app.command("/createlist")
    def handle_create_list_command(ack: Ack, body: dict, respond: Respond, client:WebClient):
        ack()
        list_name = body["text"]
        if not list_name:
            respond("Please provide a name for the list.")
            return

        try:
            new_list = create_list(list_name)
            save_list(new_list)
            respond(f"List '{list_name}' created successfully!")
        except Exception as e:
            respond(f"Error creating list: {e}")

    # Add Task
    @app.command("/addtask")
    def handle_add_task_command(ack: Ack, body: dict, respond: Respond):
        ack()
        text_parts = body["text"].split(" to ")
        if len(text_parts) != 2:
            respond("Usage: /addtask [task description] to [list name]")
            return
        task_description, list_name = text_parts
        try:
            add_task(list_name, task_description)
            respond(f"Task '{task_description}' added to '{list_name}'")
        except Exception as e:
            respond(f"Error adding task: {e}")

    # View List
    @app.command("/viewlist")
    def handle_view_list_command(ack: Ack, body: dict, respond: Respond):
        ack()
        list_name = body["text"]
        if not list_name:
            respond("Please provide the name of the list to view.")
            return

        try:
            list_data = get_list(list_name)
            if list_data:
                list_text = f"List: {list_name}\n"
                for i, task in enumerate(list_data["items"], start=1):
                    list_text += f"{i}. {task['description']} (Completed: {task['completed']})\n"
                respond(list_text)
            else:
                respond(f"List '{list_name}' not found.")
        except Exception as e:
            respond(f"Error viewing list: {e}")

    # Mark Complete
    @app.command("/markcomplete")
    def handle_mark_complete_command(ack: Ack, body: dict, respond: Respond):
        ack()
        text_parts = body["text"].split(" in ")
        if len(text_parts) != 2:
            respond("Usage: /markcomplete [task number] in [list name]")
            return

        try:
            task_number_str, list_name = text_parts
            task_number = int(task_number_str) - 1  # Convert to 0-based index
            mark_task_complete(list_name, task_number)
            respond(f"Task {task_number + 1} in '{list_name}' marked as complete.")
        except ValueError:
            respond("Invalid task number. Please provide a number.")
        except Exception as e:
            respond(f"Error marking task complete: {e}")
    
    # Delete List
    @app.command("/deletelist")
    def handle_delete_list(ack: Ack, body: dict, respond: Respond):
        ack()
        list_name = body["text"]
        if not list_name:
            respond("Please provide the name of the list to delete.")
            return
        try:
            delete_list(list_name)
            respond(f"List '{list_name}' deleted.")
        except Exception as e:
            respond(f"Error deleting list: {e}")
    # -----------------------------------------------------

    # Add command registration for other tools here
    # (e.g., slackboard, slackcalendar, etc.)
