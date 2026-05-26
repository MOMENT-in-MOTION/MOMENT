import logging

def configure_logging(verbose: bool) -> None:
    """Configure the logging settings based on the verbose flag."""
    logging.basicConfig(
        format="%(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
        level=logging.DEBUG if verbose else logging.INFO
    )
    root_logger = logging.getLogger()
    if verbose:
        root_logger.setLevel(logging.DEBUG)
        root_logger.debug("Verbose mode enabled. Logging set to DEBUG level.")
    if not verbose:
        root_logger.setLevel(logging.INFO)
        root_logger.info("Verbose mode disabled. Logging set to INFO level.")
