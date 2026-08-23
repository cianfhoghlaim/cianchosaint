// ciafagent-self-host/baml_src/clients.baml
// Self-host uses ONLY local models. No external API calls.

client<llm> SHLocalOllama {
  provider "local"
  options {
    base_url "http://localhost:11434/v1"
    model "llama3.1:8b-instruct-q5_K_M"
    temperature 0.1
  }
}

client<llm> SHLocalLlamaCpp {
  provider "local"
  options {
    base_url "http://localhost:8080/v1"
    model "gaicistral"
    temperature 0.0
  }
}

retry_policy SHRetry {
  max_attempts 2
  strategy {
    type fixed_delay
    delay_ms 1000
  }
}
