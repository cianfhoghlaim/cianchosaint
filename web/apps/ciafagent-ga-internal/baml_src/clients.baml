// ciafagent-ga-internal/baml_src/clients.baml
// Internal BAML clients — higher-rate limits + access to internal-only models

client<llm> GAInternalOpenAI {
  provider "openai"
  options {
    model "gpt-4o"
    temperature 0.1
  }
}

client<llm> GAInternalAnthropic {
  provider "anthropic"
  options {
    model "claude-3.5-sonnet"
    temperature 0.1
  }
}

// Internal-only PULSE schema lookup client
client<llm> GAPulseLookup {
  provider "openai"
  options {
    model "gpt-4o-mini"
    temperature 0.0
    base_url "https://pulse-internal.cianchosaint.ie/v1"
  }
}

// Internal circulars lookup (offline)
client<llm> GACircularsLookup {
  provider "local"
  options {
    base_url "http://localhost:11434/v1"
    model "mistral:7b"
  }
}

retry_policy GAInternalRetry {
  max_attempts 5
  strategy {
    type exponential_backoff
    initial_interval 500
    max_interval 5000
  }
}
