import os
import sys

# Set the API key
os.environ['OPENAI_API_KEY'] = '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'

# Test the LLM
from finalproject import main
import argparse

args = argparse.Namespace(prompt="add park Yellowstone", use_llm=True)
main.cmd_agent(args)
