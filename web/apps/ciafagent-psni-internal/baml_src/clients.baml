// ciafagent-psni-internal/baml_src/clients.baml

client<llm> PSNIInternalOpenAI { provider "openai" options { model "gpt-4o" temperature 0.1 } }
client<llm> PSNIPolicingBoard { provider "openai" options { model "gpt-4o-mini" temperature 0.0 base_url "https://policing-board.cianchosaint.ie/v1" } }
retry_policy PSNIInternalRetry { max_attempts 5 strategy { type exponential_backoff initial_interval 500 max_interval 5000 } }
