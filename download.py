import requests  # type: ignore[import]


def model_from_google_drive(file_id: str, destination: str) -> None:
    """
    Expects a (google drive) file ID and a destination to save it.
    Reference: https://stackoverflow.com/a/39225039
    """
    url = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(url, params={"id": file_id}, stream=True)
    response = session.get(url, params={"id": file_id, "confirm": "t"}, stream=True)

    chunk_size = 32768
    with open(destination, "wb") as file:
        for chunk in response.iter_content(chunk_size):
            if chunk:  # filters out keepalive new chunks
                file.write(chunk)


if __name__ == "__main__":
    model_from_google_drive(
        file_id="1-Yg0cxgrNhHP-016FPdp902BR-kSsA4P",
        destination="./models/u2net_human_seg.pth",
    )
