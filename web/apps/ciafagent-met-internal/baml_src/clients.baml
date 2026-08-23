// ciafagent-met-internal/baml_src/clients.baml

client<llm> METInternalOpenAI { provider "openai" options { model "gpt-4o" temperature 0.1 } }
client<llm> METInternalAnthropic { provider "anthropic" options { model "claude-3.5-sonnet" temperature 0.1 } }
client<llm> METPNCLookup { provider "openai" options { model "gpt-4o-mini" temperature 0.0 base_url "https://pnc.cianchosaint.ie/v1" } }
retry_policy METInternalRetry { max_attempts 5 strategy { type exponential_backoff initial_interval 500 max_interval 5000 } }
