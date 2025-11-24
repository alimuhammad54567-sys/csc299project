Prompt Guidelines and Useful Prompts for Speckit

Purpose
- Provide a set of prompt templates and guidance for using AI to generate, review, or refine specs, tests, and documentation for Speckit.

How to use
- Copy the prompt you want to use, fill in the placeholders, and run it in your AI assistant session.

Prompt: Generate a spec from a short brief
Input:
- Brief: "{one-line summary of feature or change}"
- Goals: "{list of goals or success criteria}"
- Constraints: "{any constraints, e.g., performance, privacy}"

Template:
"Generate a technical spec for Speckit. Use the repository's `speckit.constitution` principles: clarity, simplicity, testing standards, and UX consistency. Include: an overview, background, functional requirements, API/interface examples, tests required, acceptance criteria, and a rollback plan. Keep it concise (max 800 words)."

Prompt: Create unit tests for a given function
Input:
- File: path to file
- Function: function name
- Behavior: short description

Template:
"Write unit tests for the function `{function}` in `{file}`. Tests should be deterministic, cover happy and edge cases, and mock external dependencies. Use the project's preferred testing framework. Provide test names and short descriptions." 

Prompt: Review a spec for completeness
Template:
"Review the following spec for completeness and alignment with `speckit.constitution`. List missing requirements, unclear sections, testing gaps, and suggested acceptance criteria. Provide concise edits or bullets to fix each issue." 

Best practices
- Give precise context (file paths, example inputs) so AI generates accurate code.
- When asking for tests, specify the testing framework and whether resources (DB, network) should be mocked.
- Use the `speckit.constitution` as the default decision filter for tradeoffs and priorities.

Example usage
- "Use the 'Generate a spec' template with Brief='Add template selection UI', Goals='Allow users to pick spec templates; store selection in metadata', Constraints='No major client-side frameworks'"
