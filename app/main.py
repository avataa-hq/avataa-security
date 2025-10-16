from starlette.middleware.cors import CORSMiddleware

from init_app import create_app
from routers import roles, user_info

app_prefix = "/api/security_middleware"
app_title = "Security Middleware"

app = create_app(root_path=app_prefix)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app_v1_version = "1"
app_v1_prefix = f"{app_prefix}/v{app_v1_version}"
app_v1 = create_app(
    root_path=app_v1_prefix, title=app_title, version=app_v1_version
)
app_v1.include_router(router=roles.router)
app_v1.include_router(router=user_info.router)
app.mount("/v1", app_v1)
