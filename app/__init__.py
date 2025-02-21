def _run_as_script() -> None:
    import uvicorn
    from app.app_setup import default_app_factory

    app = default_app_factory()
    uvicorn.run(app=app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    _run_as_script()
