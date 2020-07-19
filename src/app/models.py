from typing import Optional

from pydantic import BaseModel, Field, validator


class Screenshot(BaseModel):
    url: str = Field(
        description="The URL of the page to screenshot", example="https://google.com"
    )
    window_width: int = Field(
        default=1240,
        description="Width of the headless browser window (in px)",
        example=1240,
        lt=9000,
    )
    window_height: int = Field(
        default=1854,
        description="Height of the headless browser window (in px)",
        example=1854,
        lt=9000,
    )
    export_type: Optional[str] = Field(
        default="png",
        description="Extension of the exported file (png, pdf)",
        example="png",
    )

    @validator("export_type")
    def validate_export_type(cls, v):
        assert v in ("png", "pdf"), "Only PNG and PDF exports are supported"
        return v
