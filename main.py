from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.employee import EmployeeRouter
from api.attendance import CheckingEventApiRouter
from api.breaking import BreakApiRouter
from configs.env import get_environment_variables
from metadata.tags import Tags

env = get_environment_variables()

app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(EmployeeRouter)
app.include_router(CheckingEventApiRouter)
app.include_router(BreakApiRouter)

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

