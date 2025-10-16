# Security Middleware

## Environment variables

```toml
DOCS_CUSTOM_ENABLED=<True/False>
DOCS_REDOC_JS_URL=<redoc_js_url>
DOCS_SWAGGER_CSS_URL=<swagger_css_url>
DOCS_SWAGGER_JS_URL=<swagger_js_url>
KEYCLOAK_CLIENT_ID=<keycloak_security_middleware_client>
KEYCLOAK_CLIENT_SECRET=<keycloak_security_middleware_client_secret>
KEYCLOAK_HOST=<keycloak_host>
KEYCLOAK_PORT=<keycloak_port>
KEYCLOAK_PROTOCOL=<keycloak_protocol>
KEYCLOAK_REALM=avataa
KEYCLOAK_REDIRECT_HOST=<keycloak_external_host>
KEYCLOAK_REDIRECT_PORT=<keycloak_external_port>
KEYCLOAK_REDIRECT_PROTOCOL=<keycloak_external_protocol>
REDIS_DB=<redis_db>
REDIS_HOST=<redis_host>
REDIS_PORT=<redis_port>
UVICORN_WORKERS=<uvicorn_workers_number>
```

### Explanation

#### Compose

- `REGISTRY_URL` - Docker regitry URL, e.g. `harbor.domain.com`
- `PLATFORM_PROJECT_NAME` - Docker regitry project Docker image can be downloaded from, e.g. `avataa`