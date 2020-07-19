from .app import app

from mangum import Mangum

handler = Mangum(app, lifespan="off")


if __name__ == "__main__":
    # To run this locally
    import uvicorn

    uvicorn.run(app, debug=True)
