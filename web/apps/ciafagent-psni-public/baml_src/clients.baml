// ciafagent-psni-public/baml_src/clients.baml

client<llm> PSNIOpenAI { provider "openai" options { model "gpt-4o" temperature 0.1 } }
client<llm> PSNIAnthropic { provider "anthropic" options { model "claude-3.5-sonnet" temperature 0.1 } }
client<llm> PSNIPolicingBoard { provider "openai" options { model "gpt-4o-mini" temperature 0.0 } }
retry_policy PSNIRetry { max_attempts 3 strategy { type exponential_backoff initial_interval 1000 max_interval 10000 } }
