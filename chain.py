# chain.py
import os

from langchain_core.messages import AIMessage
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
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

        self.current_task_tree = ""

        # Initialize the conversation
        self._initialize_chain(target)

    def _initialize_chain(self, target: str):
        # Create an executable sequence
        chain = PromptTemplate(template=BASE_SYSTEM_PROMPT, input_variables=["target"]) | self.llm

        # Generate the initial tree
        self.current_task_tree = chain.invoke({"target": target}).content

    def update_task_tree_with_output(self, output_text: str):
        """
        Updates the task tree according to the new output (command result).
        """
        # Create a context from the current tree and results
        context = (f"Current Task Tree:\n"
                   f"{self.current_task_tree}\n\n"
                   f"Tool Output:\n"
                   f"{output_text}")

        # Create an executable sequence for update
        chain = PromptTemplate(template=CONTEXT_PROMPT, input_variables=["context"]) | self.llm

        # Generate the updated tree
        updated_tree = chain.invoke({"context": context})

        # Update the tree locally
        self.current_task_tree = updated_tree.content
        return self.current_task_tree

    def get_current_task_tree(self):
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

