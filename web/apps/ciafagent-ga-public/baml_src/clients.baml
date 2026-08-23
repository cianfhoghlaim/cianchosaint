// ciafagent-ga-public/baml_src/clients.baml
// Per-app BAML client for the ga_root_agent
// Per the 4-tier provider chain spec:
//   tier 1 — ga_root_agent (primary)
//   tier 2 — GA specialists (IrishStatuteBookAgent, GATrafficLawAgent, etc.)
//   tier 3 — cross_jurisdiction_query (GA ↔ MET ↔ PSNI)
//   tier 4 — local fallback (offline / cached responses)

client<llm> GAOpenAI {
  provider "openai"
  options {
    model "gpt-4o"
    temperature 0.1
  }
}

client<llm> GAAnthropic {
  provider "anthropic"
  options {
    model "claude-3.5-sonnet"
    temperature 0.1
  }
}

client<llm> GAGoogle {
  provider "google"
  options {
    model "gemini-1.5-pro"
    temperature 0.1
  }
}

client<llm> GALocalFallback {
  provider "local"
  options {
    base_url "http://localhost:11434/v1"
    model "llama3.1:8b"
  }
}

// Retry policy: 3 attempts with exponential backoff
retry_policy GARetry {
  max_attempts 3
  strategy {
    type exponential_backoff
    initial_interval 1000
    max_interval 10000
  }
}
