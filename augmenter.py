def build_context(results):
    context = ""

    for i in range(len(results["documents"][0])):
        source = results["metadatas"][0][i]["source"]
        chunk = results["documents"][0][i]

        context += f"Source: {source}\n"
        context += f"Content: {chunk}\n\n"

    return context


def build_prompt(query, context):
    return f"""
You are an academic assistant for university policy questions.

Answer ONLY using the provided context.
If the context does not clearly contain the answer, say so clearly.

Formatting requirements:
- Use plain text only (NO markdown symbols like **, *, #, tables)
- Keep responses clean, structured, and easy to read
- Use spacing between sections
- Use bullet points with "-" where appropriate
- Organize information logically with clear headings in plain text
- If multiple cases or exceptions exist, separate them clearly
- Do NOT dump raw policy text unless necessary
- Summarize in natural student-friendly language while preserving accuracy

User question:
{query}

Context:
{context}
"""