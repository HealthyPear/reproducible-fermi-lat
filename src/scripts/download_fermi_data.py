"""Load url_filnames.txt and download all files in parallel.

Parallelism is achieved by multiprocessing from a single master process.
Checksum is not validated.
"""

import concurrent.futures
import logging
from ast import literal_eval as make_tuple
from pathlib import Path
import threading
from urllib.request import urlopen

from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

import paths

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def download_file_with_progress(url, output_path):
    """Download the file from url to filename if the file doesn't exist or checksum is different, with progress bar."""
    if Path(output_path).exists():
        logger.info(f"File {output_path} exists. Skipping download.")
        return

    try:
        with urlopen(url) as response:
            total_size = int(response.getheader("Content-Length").strip())
            block_size = 8192
            with (
                open(output_path, "wb") as f,
                tqdm(
                    desc=f"Downloading {output_path}",
                    total=total_size,
                    unit="iB",
                    unit_scale=True,
                    leave=False,
                    ncols=progress_bar_width,
                    colour="green",
                ) as inner_pbar,
            ):
                while not stop_event.is_set():
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    f.write(buffer)
                    inner_pbar.update(len(buffer))
        logger.info(f"Downloaded {url} to {output_path}")
    except Exception as e:
        logger.exception(f"Failed to download {url}: {e}")
        raise


data_path = paths.data
fermi_data = data_path / "Fermi_LAT"
fermi_data.mkdir(parents=False, exist_ok=True)

# Flag to signal threads to stop
stop_event = threading.Event()

progress_bar_width = None

with open(Path(fermi_data / "url_filenames.txt"), mode="r", encoding="utf-8") as f:
    lines = f.readlines()
urls_filenames = [make_tuple(line) for line in lines]

try:
    with logging_redirect_tqdm():
        # Using ThreadPoolExecutor to download files in parallel
        with (
            concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor,
            tqdm(
                total=len(urls_filenames), ncols=progress_bar_width, colour="blue"
            ) as outer_pbar,
        ):
            # Mapping download_file function to the list of (url, filename) tuples
            futures = [
                executor.submit(download_file_with_progress, url, filename)
                for url, filename in urls_filenames
            ]

            # Ensuring all futures are completed
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.exception(f"Error occurred during download: {e}")
                    raise
                outer_pbar.update(1)
except KeyboardInterrupt:
    stop_event.set()
    print("Interrupted by user. Cancelling all downloads...")
    for future in futures:
        future.cancel()
