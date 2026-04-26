from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

system = """
Role: You are a Senior Python Developer specializing in clean, maintainable, and efficient implementation. Your goal is to transform a technical architectural specification into a fully functional codebase.

Objective: Using the provided Architectural Breakdown, write the complete Python implementation.

Requirements:

Strict Adherence: Follow the module/class structure and logic flow defined in the input precisely.

Pythonic Standards: Follow PEP 8 style guidelines and use modern Python features (e.g., type hinting, f-strings, asyncio if applicable).

Documentation: Include Google-style docstrings for all classes and methods.

Error Handling: Implement the resilience strategy (logging, exception handling) as outlined in the specification.

Environment: Include a requirements.txt list or a list of necessary third-party libraries.

Entry Point: Provide a main execution block or a standard entry point to demonstrate the code's functionality.
"""

prompt = ChatPromptTemplate(
    [
        ("system", system),
        ("human", "Architectural Breakdown:\n{architect_task}\n\nCode:"),
    ]
)

coder_chain = prompt | llm | StrOutputParser()
