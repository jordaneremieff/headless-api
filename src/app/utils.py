import os
import base64
from uuid import uuid4
from typing import Union
from io import BytesIO

import boto3
from botocore.config import Config
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .models import Screenshot


CHROME_BINARY_PATH = os.getenv(
    "CHROME_BINARY_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", "/usr/local/bin/chromedriver")
CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36"
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "headless-api-uploads")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument(f"--user-agent={CHROME_USER_AGENT}")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("prefs", {"enable_do_not_track": True})
chrome_options.binary_location = CHROME_BINARY_PATH


def generate_file(screenshot: Screenshot) -> Union[bytes, str, str]:
    file_name = f"{uuid4()}.{screenshot.export_type}"
    media_type = "application/pdf" if screenshot.export_type == "pdf" else "image/png"
    with webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH, options=chrome_options
    ) as driver:
        driver.set_window_size(screenshot.window_width, screenshot.window_height)
        driver.get(screenshot.url)
        img_data = driver.get_screenshot_as_base64()

    png_data = BytesIO(base64.b64decode(img_data))

    if screenshot.export_type == "png":
        return png_data, file_name, media_type

    src_img = Image.open(png_data)
    pdf_data = BytesIO()
    rgb = Image.new("RGB", src_img.size, (255, 255, 255))
    rgb.paste(src_img, mask=src_img.split()[3])
    rgb.save(pdf_data, format="PDF")

    return pdf_data, file_name, media_type


def upload_file(file_data: bytes, *, file_name: str, source_url: str) -> str:
    client = boto3.client(
        "s3", config=Config(connect_timeout=5, retries={"max_attempts": 3})
    )
    client.upload_fileobj(
        file_data,
        Bucket=S3_BUCKET_NAME,
        Key=file_name,
        ExtraArgs={"Metadata": {"source_url": source_url}},
    )
    presigned_url = client.generate_presigned_url(
        "get_object", Params={"Bucket": S3_BUCKET_NAME, "Key": file_name}, ExpiresIn=100
    )

    return presigned_url


def get_file_count() -> int:
    resource = boto3.resource("s3")
    bucket = resource.Bucket(S3_BUCKET_NAME)

    return sum(1 for _ in bucket.objects.all())
