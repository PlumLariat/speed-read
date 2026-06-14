import logging
import subprocess

logger = logging.getLogger(__name__)


def is_ollama_installed() -> bool:
    """Checks if [ollama](https://ollama.com/) is installed on the system where function is run.

    Returns:
        Boolean value which represents installation status of ollama.
    """
    try:
        sp = subprocess.run(["ollama", "--version"], capture_output=True)
        logger.info(f"ollama {sp.stdout.decode().strip()} installed.")
        return sp.returncode == 0
    except FileNotFoundError:
        logger.debug("ollama not found on system.")
        return False


# def install_ollama()


def is_tesseract_installed() -> bool:
    """Checks if [tesseract](https://github.com/tesseract-ocr/tesseract) is installed on the system where function is run.

    Returns:
        Boolean value which represents installation status of tesseract.
    """
    try:
        sp = subprocess.run(["tesseract", "--version"], capture_output=True)
        if sp.returncode != 0:
            logger.debug("tesseract returned a non-zero exit code.")
            return False
        logger.info(f"tesseract version: {sp.stdout.decode().split()[1]} installed.")
        return True
    except FileNotFoundError:
        logger.debug("tesseract not found on system.")
        return False


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    is_ollama_installed()
    is_tesseract_installed()
