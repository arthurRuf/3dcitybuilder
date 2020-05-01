import urllib, sys,requests
from . import progress_bar

def download_file(url, file_destination):
    with open(file_destination, "wb") as f:
        print("Downloading...")
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
            print("Unable to retrieve file size. You will be informed when the download has finished. It might take a while")
            urllib.request.urlretrieve(url, file_destination)
            print("Done!")
        else:
            dl = 0
            total_length = int(total_length)

            chunk_size = 1024
            progress_bar_helper = progress_bar.create(total_length/chunk_size)
            for data in response.iter_content(chunk_size=chunk_size):
                dl += len(data)
                progress_bar.update(progress_bar_helper)
                f.write(data)

            progress_bar.done(progress_bar_helper)

