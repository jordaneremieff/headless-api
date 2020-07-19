from typing import Optional

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse


from .models import Screenshot
from .utils import generate_file, upload_file


app = FastAPI(
    title="Headless API",
    description="Python API service for headless Chromium",
    version="0.0.1",
)


@app.post(
    "/screenshot",
    responses={
        200: {
            "description": "Export file or S3 URL for a page screenshot.",
            "content": {
                "application/json": {
                    "example": {
                        "url": "s3://my-export-bucket-123/export-file-123.png",
                        "message": "Message description",
                    }
                },
                "application/pdf": {},
                "image/png": {},
            },
        }
    },
)
def screenshot_page(screenshot: Screenshot, upload_to_s3: Optional[bool] = False):
    file_data, file_name, media_type = generate_file(screenshot)
    file_data.seek(0)

    if upload_to_s3:
        url = upload_file(file_data, file_name=file_name, source_url=screenshot.url)
        return {"url": url}

    return StreamingResponse(
        file_data,
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
        media_type=media_type,
    )


@app.get("/")
def redirect():
    return RedirectResponse("/docs")
