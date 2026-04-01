# What RAG Adds

Normal chatting is often enough for general knowledge questions.

It is not enough when the answer depends on:

- local workshop notes
- private or niche domain context
- details that the base model is unlikely to know
- exact phrasing from project-specific material

Retrieval-Augmented Generation adds a retrieval step before answering:

1. embed the user question
2. search local content for relevant chunks
3. inject those chunks into the prompt
4. let the model answer with that grounded context

For this workshop, RAG is intentionally designed to answer questions such as:

- What is the HH Nerd Gruppe context for this session?
- How is the Java workshop positioned against the Python workshop?
- Why does the workshop avoid framework magic?

These are not broad internet facts. They are local workshop facts. That is why retrieval helps.
