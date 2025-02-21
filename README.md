# Everything API

An AI-powered API that does not exist, yet does everything.

## How it works

It works by delegating the response generation to an LLM model running with ollama, somewhere.

## Running locally

With the power of Docker, this task becomes simple:

```shell
docker compose up 
```

This will download the start a container with the api, a container with ollama, and another container that's responsible
for downloading the desired ollama model. This model is grabbed from the .env file, variable 
`EVERYTHING_API_OLLAMA_MODEL`.

## What's the point?

This is a simple proof-of-concept of how one can use LLMs easily with Python.

I believe there could be some potential security benefits to make a scraper's life harder by allowing him to call every
endpoint imaginable, even if it doesn't actually serve any purpose.

> In the realm of API security, obscurity through infinite possibility becomes a feature rather than a flaw.
>
> &mdash; <cite>Schrödinger's API Principle by R1, Deepseek (circa 2025 BC)</cite>
