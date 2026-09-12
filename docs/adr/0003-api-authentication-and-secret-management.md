# ADR-0003: API Authentication and Secret Management

- **Status:** Accepted
- **Date:** 2026-09-12
- **Decision Type:** Security / API Design

## Context and Problem Statement

`Srivatsasa-capstone` does not currently implement endpoint-level authentication. Its security approach manages the `OPENAI_API_KEY` as a server-side environment credential, while API authentication was explicitly outside the scope of its v1 API contract.

`M1_EKA_Gorthi` requires API-level authentication while retaining secure, server-side management of the OpenAI credential.

## Decision Drivers

- Protect M1 API endpoints from unauthorized access.
- Keep `OPENAI_API_KEY` server-side and prevent exposure to API clients.
- Maintain a clear separation between API authentication and LLM-provider authentication.
- Avoid modifying `Srivatsasa-capstone`.
- Provide a simple authentication mechanism appropriate for the current M1 scope.
- Allow the authentication approach to evolve to enterprise authentication in a future phase.

## Considered Options

1. **Separate Bearer-token authentication for the M1 API**
2. **Use `OPENAI_API_KEY` as the API authentication token**
3. **Add endpoint authentication to `Srivatsasa-capstone`**
4. **No API authentication**
5. **Use enterprise OAuth2/OIDC**

## Decision Outcome

**Chosen option: Separate Bearer-token authentication for the M1 API.**

`M1_EKA_Gorthi` will:

- Use `Authorization: Bearer <token>` for API-level authentication.
- Keep `OPENAI_API_KEY` as a server-side environment variable.
- Never expose the OpenAI credential to API clients.
- Treat API authentication and OpenAI authentication as independent security layers.
- Leave `Srivatsasa-capstone` unchanged.

The resulting security flow is:

```text
API Client
    |
    | Authorization: Bearer <API token>
    v
M1_EKA_Gorthi API
    |
    | OPENAI_API_KEY
    | (server-side environment variable)
    v
OpenAI API