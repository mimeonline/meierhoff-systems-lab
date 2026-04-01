type ChatResponse = {
  sessionId: string;
  phase: string;
  answer: string;
  comparisons: ComparisonResult[];
};

type ComparisonResult = {
  phase: string;
  title: string;
  answer: string;
};

type DebugSnapshot = {
  sessionId: string;
  phase: string;
  prompt: string;
  memory: string[];
  toolCalls: ToolCall[];
  retrievals: Retrieval[];
  comparisons: ComparisonResult[];
};

type ToolCall = {
  toolName: string;
  arguments: string;
  result: string;
};

type Retrieval = {
  source: string;
  score: number;
  snippet: string;
};

const phaseSuggestions: Record<string, string[]> = {
  "phase-1-chat": [
    "What is LangChain4j in one paragraph?",
    "Why does plain chat struggle with workshop-specific facts?"
  ],
  "phase-2-memory": [
    "My name is Hannah. Please remember it.",
    "What did I tell you about my name?"
  ],
  "phase-3-tool": [
    "What time is it in Berlin right now?",
    "Please calculate 18.5 multiplied by 7."
  ],
  "phase-4-mcp": [
    "Use MCP to inspect the workshop files and explain the Java workshop goal.",
    "Which workshop note talks about Tool Usage vs MCP?"
  ],
  "phase-5-rag": [
    "Why is normal chatting not enough for this workshop context?",
    "Explain the difference between the Python workshop and the Java workshop with sources."
  ],
  "phase-6-compare": [
    "Compare how the system answers questions about workshop-specific facts.",
    "What changes when the agent has memory, tools, and retrieval?"
  ]
};

const phaseDescriptions: Record<string, string> = {
  "phase-1-chat": "Single-turn baseline. No memory, no tools, no retrieval.",
  "phase-2-memory": "Conversation state stays around. Follow-up questions become grounded in previous turns.",
  "phase-3-tool": "The model can call local Java tools for deterministic operations.",
  "phase-4-mcp": "The model can bridge to external tools through MCP instead of direct Java methods.",
  "phase-5-rag": "Local workshop notes are retrieved semantically and injected as context.",
  "phase-6-compare": "Multiple variants run side by side so participants can compare answer behavior."
};

const chatLog = document.querySelector<HTMLDivElement>("#chatLog");
const debugPanel = document.querySelector<HTMLDivElement>("#debugPanel");
const form = document.querySelector<HTMLFormElement>("#chatForm");
const messageInput = document.querySelector<HTMLTextAreaElement>("#message");
const phaseInput = document.querySelector<HTMLSelectElement>("#phase");
const sessionInput = document.querySelector<HTMLInputElement>("#sessionId");
const suggestions = document.querySelector<HTMLDivElement>("#suggestions");
const newSessionButton = document.querySelector<HTMLButtonElement>("#newSession");
const sendButton = document.querySelector<HTMLButtonElement>("#send");

if (!chatLog || !debugPanel || !form || !messageInput || !phaseInput || !sessionInput || !suggestions || !newSessionButton || !sendButton) {
  throw new Error("Frontend could not initialize because required elements are missing.");
}

const chatLogElement = chatLog;
const debugPanelElement = debugPanel;
const formElement = form;
const messageInputElement = messageInput;
const phaseInputElement = phaseInput;
const sessionInputElement = sessionInput;
const suggestionsElement = suggestions;
const newSessionButtonElement = newSessionButton;
const sendButtonElement = sendButton;

sessionInputElement.value = crypto.randomUUID();
renderSuggestions(phaseInputElement.value);
renderDebugPanel(emptyDebug(phaseInputElement.value));

phaseInputElement.addEventListener("change", () => {
  renderSuggestions(phaseInputElement.value);
  renderDebugPanel(emptyDebug(phaseInputElement.value));
});

newSessionButtonElement.addEventListener("click", () => {
  sessionInputElement.value = crypto.randomUUID();
  chatLogElement.innerHTML = "";
  renderDebugPanel(emptyDebug(phaseInputElement.value));
});

formElement.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = messageInputElement.value.trim();
  if (!message) {
    return;
  }

  const sessionId = sessionInputElement.value.trim() || crypto.randomUUID();
  sessionInputElement.value = sessionId;
  const phase = phaseInputElement.value;

  appendMessage("You", message, "message-user");
  messageInputElement.value = "";
  sendButtonElement.disabled = true;
  sendButtonElement.textContent = "Thinking...";

  try {
    const response = await sendChat({ phase, sessionId, message });
    appendAssistantResponse(response);
    const debug = await loadDebug(phase, response.sessionId);
    renderDebugPanel(debug);
  } catch (error) {
    appendMessage("System", error instanceof Error ? error.message : "Request failed", "message-ai");
  } finally {
    sendButtonElement.disabled = false;
    sendButtonElement.textContent = "Send";
  }
});

function renderSuggestions(phase: string) {
  suggestionsElement.innerHTML = "";
  for (const example of phaseSuggestions[phase] ?? []) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "rounded-full border border-black/10 bg-white px-3 py-2 text-xs font-medium text-ink/70 transition hover:border-moss hover:text-moss";
    button.textContent = example;
    button.addEventListener("click", () => {
      messageInputElement.value = example;
      messageInputElement.focus();
    });
    suggestionsElement.appendChild(button);
  }
}

function appendAssistantResponse(response: ChatResponse) {
  appendMessage("AI", response.answer, "message-ai");
  if (response.comparisons.length > 0) {
    const container = document.createElement("div");
    container.className = "message-card message-ai space-y-3";
    const title = document.createElement("p");
    title.className = "font-mono text-xs uppercase tracking-[0.28em] text-moss";
    title.textContent = "Comparison variants";
    container.appendChild(title);

    for (const comparison of response.comparisons) {
      const block = document.createElement("div");
      block.className = "rounded-2xl border border-black/5 bg-[#f8f4eb] p-3";
      block.innerHTML = `
        <p class="font-semibold text-sm text-ink">${escapeHtml(comparison.title)}</p>
        <p class="mt-2 text-sm leading-6 text-ink/80 whitespace-pre-wrap">${escapeHtml(comparison.answer)}</p>
      `;
      container.appendChild(block);
    }

    chatLogElement.appendChild(container);
    chatLogElement.scrollTop = chatLogElement.scrollHeight;
  }
}

function appendMessage(label: string, text: string, typeClass: string) {
  const wrapper = document.createElement("article");
  wrapper.className = `message-card ${typeClass}`;
  wrapper.innerHTML = `
    <p class="font-mono text-xs uppercase tracking-[0.28em] text-moss">${escapeHtml(label)}</p>
    <p class="mt-3 whitespace-pre-wrap text-sm leading-7 text-ink/85">${escapeHtml(text)}</p>
  `;
  chatLogElement.appendChild(wrapper);
  chatLogElement.scrollTop = chatLogElement.scrollHeight;
}

function renderDebugPanel(debug: DebugSnapshot) {
  debugPanelElement.innerHTML = "";
  debugPanelElement.appendChild(createDebugCard("Current phase", phaseDescriptions[debug.phase] ?? debug.phase));
  debugPanelElement.appendChild(createCodeCard("Prompt", debug.prompt || "No prompt captured yet."));
  debugPanelElement.appendChild(createListCard("Memory", debug.memory.length > 0 ? debug.memory : ["No memory entries for this phase yet."]));
  debugPanelElement.appendChild(createListCard("Tool calls", debug.toolCalls.length > 0 ? debug.toolCalls.map(formatToolCall) : ["No tool calls recorded."]));
  debugPanelElement.appendChild(createListCard("RAG context", debug.retrievals.length > 0 ? debug.retrievals.map(formatRetrieval) : ["No retrieval results recorded."]));

  if (debug.comparisons.length > 0) {
    debugPanelElement.appendChild(createListCard("Comparisons", debug.comparisons.map((entry) => `${entry.title}: ${entry.answer}`)));
  }
}

function createDebugCard(title: string, body: string): HTMLElement {
  const section = document.createElement("section");
  section.className = "debug-card";
  section.innerHTML = `
    <p class="font-mono text-[11px] uppercase tracking-[0.28em] text-sand/75">${escapeHtml(title)}</p>
    <p class="mt-3 text-sm leading-6 text-white/80">${escapeHtml(body)}</p>
  `;
  return section;
}

function createCodeCard(title: string, body: string): HTMLElement {
  const section = document.createElement("section");
  section.className = "debug-card";
  section.innerHTML = `
    <p class="font-mono text-[11px] uppercase tracking-[0.28em] text-sand/75">${escapeHtml(title)}</p>
    <pre class="mt-3 overflow-x-auto whitespace-pre-wrap rounded-2xl bg-black/15 p-3 font-mono text-xs leading-6 text-sand">${escapeHtml(body)}</pre>
  `;
  return section;
}

function createListCard(title: string, items: string[]): HTMLElement {
  const section = document.createElement("section");
  section.className = "debug-card";

  const heading = document.createElement("p");
  heading.className = "font-mono text-[11px] uppercase tracking-[0.28em] text-sand/75";
  heading.textContent = title;
  section.appendChild(heading);

  const list = document.createElement("div");
  list.className = "mt-3 space-y-2";

  for (const item of items) {
    const row = document.createElement("div");
    row.className = "rounded-2xl bg-black/15 px-3 py-2 text-sm leading-6 text-white/80";
    row.textContent = item;
    list.appendChild(row);
  }

  section.appendChild(list);
  return section;
}

async function sendChat(payload: { phase: string; sessionId: string; message: string }): Promise<ChatResponse> {
  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(body);
  }

  return response.json();
}

async function loadDebug(phase: string, sessionId: string): Promise<DebugSnapshot> {
  const response = await fetch(`/debug?phase=${encodeURIComponent(phase)}&sessionId=${encodeURIComponent(sessionId)}`);
  if (!response.ok) {
    const body = await response.text();
    throw new Error(body);
  }
  return response.json();
}

function formatToolCall(toolCall: ToolCall): string {
  return `${toolCall.toolName} | args=${toolCall.arguments} | result=${toolCall.result}`;
}

function formatRetrieval(retrieval: Retrieval): string {
  return `${retrieval.source} | score=${retrieval.score.toFixed(3)} | ${retrieval.snippet}`;
}

function emptyDebug(phase: string): DebugSnapshot {
  return {
    sessionId: sessionInputElement.value,
    phase,
    prompt: "",
    memory: [],
    toolCalls: [],
    retrievals: [],
    comparisons: []
  };
}

function escapeHtml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}
