from core.dependencies import is_ollama_installed, is_tesseract_installed


def test_returns_true_when_ollama_found(mocker):
    mock_run = mocker.patch("core.dependencies.subprocess.run")
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = b"ollama version 0.3.0\n"

    assert is_ollama_installed() is True


def test_returns_false_when_ollama_returns_nonzero(mocker):
    mock_run = mocker.patch("core.dependencies.subprocess.run")
    mock_run.return_value.returncode = 1
    mock_run.return_value.stdout = b""

    assert is_ollama_installed() is False


def test_returns_false_when_ollama_not_found(mocker):
    mocker.patch("core.dependencies.subprocess.run", side_effect=FileNotFoundError)

    assert is_ollama_installed() is False


def test_returns_true_when_tesseract_found(mocker):
    mock_run = mocker.patch("core.dependencies.subprocess.run")
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = b"tesseract 5.5.0\n leptonica-1.84.1\n  libgif 5.2.2 : libjpeg 6b (libjpeg-turbo 2.1.5) : libpng 1.6.48 : libtiff 4.7.0 : zlib 1.3.1 : libwebp 1.5.0 : libopenjp2 2.5.3\n Found AVX2\n Found AVX\n Found FMA\n Found SSE4.1\n Found OpenMP 201511\n Found libarchive 3.7.4 zlib/1.3.1 liblzma/5.8.1 bz2lib/1.0.8 liblz4/1.10.0 libzstd/1.5.7\n Found libcurl/8.14.1 OpenSSL/3.5.6 zlib/1.3.1 brotli/1.1.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.2 libssh2/1.11.1 nghttp2/1.64.0 librtmp/2.3 OpenLDAP/2.6.10\n"

    assert is_tesseract_installed() is True


def test_returns_false_when_tesseract_returns_nonzero(mocker):
    mock_run = mocker.patch("core.dependencies.subprocess.run")
    mock_run.return_value.returncode = 1
    mock_run.return_value.stdout = b""

    assert is_tesseract_installed() is False


def test_returns_false_when_tesseract_not_found(mocker):
    mocker.patch("core.dependencies.subprocess.run", side_effect=FileNotFoundError)

    assert is_tesseract_installed() is False
