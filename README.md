# chain-rock
quick demo to connect langchain, langsmith and bedrock for streaming test

## required env variables
the `aws` creds are required for authenticating to Bedrock and the `langchain` variables and keys link conversations to LangSmith.

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT='https://api.smith.langchain.com'
LANGCHAIN_API_KEY
```

## references
- [Building with Anthropic's Claude 3 on Amazon Bedrock and LangChain](https://medium.com/@dminhk/building-with-anthropics-claude-3-on-amazon-bedrock-and-langchain-%EF%B8%8F-2b842f9c0ca8)