// ciafagent-api/baml_src/clients.baml
// The gateway uses a 4-tier BAML provider chain:
//   tier 1 — primary LLM (gpt-4o or claude-3.5-sonnet)
//   tier 2 — fallback LLM (gpt-4o-mini)
//   tier 3 — cross-jurisdiction cascade (MET fallback for GA queries, etc.)
//   tier 4 — local Ollama (offline / cost guardrail)

client<llm> APIPrimaryOpenAI {
  provider "openai"
  options { model "gpt-4o" temperature 0.1 }
}

client<llm> APIPrimaryAnthropic {
  provider "anthropic"
  options { model "claude-3.5-sonnet" temperature 0.1 }
}

client<llm> APIFallback {
  provider "openai"
  options { model "gpt-4o-mini" temperature 0.1 }
}

client<llm> APIOllamaFallback {
  provider "local"
  options {
    base_url "http://localhost:11434/v1"
    model "llama3.1:70b-instruct-q5_K_M"
  }
}

retry_policy APIRetry {
  max_attempts 5
  strategy { type exponential_backoff initial_interval 1000 max_interval 30000 }
}
