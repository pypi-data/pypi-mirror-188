from locdata.logger import logger
from ensure import ensure_annotations


@ensure_annotations
def addu(a: int) -> int:
    logger.info(f"values is {a}")
    return 2 * a
