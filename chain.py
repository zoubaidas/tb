import os

from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI  # Corrected import
from langchain.schema.runnable import RunnableSequence
from langchain.prompts import PromptTemplate

from prompts import BASE_SYSTEM_PROMPT, CONTEXT_PROMPT


class TaskTreeChain:
    """
    Manages the logic for generating and updating the task tree for penetration testing.
    """

    def __init__(self, target: str):

        # Conversation model
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model="google/gemini-pro-1.5"
        )

        self.current_task_tree = ""

        # Initialize the conversation
        self.system_message = SystemMessage(content=BASE_SYSTEM_PROMPT.format(target=target))


        response = self.llm.invoke([self.system_message])
        # Store the result
        self.current_task_tree = response.content


    def update_task_tree_with_output(self, output_text: str):
        """
        Updates the task tree according to the new output (command result).
        """
        # Create a context from the current tree and results
        context = (f"Current Task Tree:\n"
                   f"{self.current_task_tree}\n\n"
                   f"Tool Output:\n"
                   f"{output_text}")


        # Format context prompt
        context_prompt = HumanMessage(content=CONTEXT_PROMPT.format(context=context))
        # Invoke the LLM with the combined context and system message
        response = self.llm.invoke([self.system_message, context_prompt])

        # Update the local tree
        self.current_task_tree = response.content
        return self.current_task_tree

    def get_current_task_tree(self):
        """
        Returns the current task tree.
        """
        return self.current_task_tree

    def get_next_command(self):
        """
        Extracts the "Run command: ..." line from the end of the task tree.
        """
        lines = self.current_task_tree.strip().splitlines()
        command = None
        for line in reversed(lines):
            if line.startswith("Run command:") and len(line) > 12:
                command = line[12:].strip()
            elif line.startswith("`Run command:") and len(line) > 13:
                command = line[13:].strip()

            if command.startswith("`"):
                command = command[1:]
            if command.endswith("`"):
                command = command[:-1]
            return command