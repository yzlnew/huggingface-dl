import argparse
from pathlib import Path
from urllib.parse import quote_plus
import requests
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description='Process input parameters.')

    parser.add_argument('folder_name', type=str, help='Name of the local folder of target repo, without lfs.')
    parser.add_argument('--repo', type=str, help='Huggingface repo name, e.g. liwu/MNBNV')
    parser.add_argument('--category', type=str, default='datasets', help='Download category. Default is "datasets".')
    parser.add_argument('--proxy', type=str, required=True, help='Cloudflare proxy to accelerate.')
    parser.add_argument('--patterns', type=str, nargs='+', help='Patterns for filtering files, e.g. *.jsonl')
    parser.add_argument('--exclude', type=str, default=None)

    args = parser.parse_args()

    print(f"Folder Name: {args.folder_name}")
    print(f"Category: {args.category}")
    print(f"Downloading Patterns: {args.patterns}")

    local_path = Path(args.folder_name)
    proxy_head = args.proxy
    repo = args.repo
    base_url = f"https://huggingface.co/{args.category}/{repo}"
    exclude = args.exclude

    file_ls = []
    for p in args.patterns:
        file_ls.extend(local_path.rglob(p))

    print(f"Total Files: {len(file_ls)}")

    failed_ls = []

    for f in file_ls:
        fname = f.relative_to(local_path).as_posix()
        if exclude is not None:
            if exclude in fname:
                print(f"{fname} is excluded!")
                continue
        if f.stat().st_size > 10 * 1024:
            print(f"Seems like {fname} is already downloaded, pass.")
            continue
        print(f"Start downloading {fname}")
        url = proxy_head + "/" + quote_plus(base_url + "/resolve/main/" + fname)

        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
        if response.status_code == 200:
            with open(f, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        progress_bar.update(len(chunk))

            progress_bar.close()
        else:
            print(f'Failed：{response.status_code}')
            failed_ls.append(fname)

    print(f"Failed files: {failed_ls}")

if __name__ == "__main__":
    main()