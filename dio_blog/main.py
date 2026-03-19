from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from dio_blog.controller import post
from dio_blog.database import database, metadata, engine
from dio_blog.views.exceptions import NotFoundPostError


@asynccontextmanager
async def lifespan(app: FastAPI):
    from dio_blog.model.post import posts
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

@app.exception_handler(NotFoundPostError)
async def not_found_post_handler(request: Request, exc: NotFoundPostError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

from fastapi.responses import JSONResponse
from dio_blog.views.exceptions import DuplicatePostError


@app.exception_handler(DuplicatePostError)
async def duplicate_post_handler(request, exc: DuplicatePostError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message}
    )

app.include_router(post.router)