# Headless API

Python API service for headless Chromium.

This project consists of a [FastAPI](https://fastapi.tiangolo.com/) application for running [headless Chromium](https://chromium.googlesource.com/chromium/src/+/lkgr/headless/README.md) browser commands using [Selenium](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver), and includes an example [Serverless](https://www.serverless.com/) configuration for AWS Lambda & API Gateway deployments that requires [Serverless-Chrome](https://github.com/adieuadieu/serverless-chrome) and [ChromeDriver](https://chromedriver.chromium.org/) binaries for headless Chromium support and [Mangum](https://mangum.io/) to wrap the ASGI application.

It is also possible to use this with a normal Chrome/Chromium binary and ASGI server (such as [Uvicorn](https://www.uvicorn.org/) or [Hypercorn](https://pgjones.gitlab.io/hypercorn/), but my intention is to demonstrate a serverless example. 

*Note*: This is a proof-of-concept/example that I created to experiment with FastAPI and serverless. I do not intend to actively maintain it.

## Usage

Live: https://headless-api.eremieff.com/

You can play around with the generated API docs in the testing deployment docs to see how it works.

<img src="https://github.com/jordaneremieff/headless-api/blob/main/assets/example.png?raw=true" alt='Headless API example'>



## Serverless deployment

You'll need to modify the `serverless.yml` file and change occurences of `headless-api` in your project. I've only confirmed this working with 3.7 and have not tested other configurations.

The following binaries must be included in the `src/bin/` directory:

```shell
curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
unzip chromedriver.zip -d src/bin/
rm chromedriver.zip
```


```shell
mkdir -p bin/
curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
unzip headless-chromium.zip -d src/bin/
rm headless-chromium.zip
```

## Running locally

To run the project locally, you'll need binaries specifc to your operation system and a normal ASGI server for the application. The local application can be run using Uvicorn:

```shell
python -m src.asgi
```

## Known Issues

- It is currently not possible to screenshot all of the content on a page if the page height is greater than the window height size.

- Some sites (e.g. GitHub) are able to detect something off about the request (an unsupported browser banner is returned in the response).
