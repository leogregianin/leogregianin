import pathlib
import time

import typer
import httpx


app = typer.Typer()

def download(path, *args, **kwargs):
    with httpx.stream('GET', *args, **kwargs) as response:
        response.raise_for_status()

        with path.open(mode='wb', buffering=0) as f:
            for chunk in response.iter_bytes(16384):
                f.write(chunk)

def download_file(path, *args, **kwargs):
    for _ in range(600):
        try:
            download(path, *args, **kwargs)
        except Exception:
            time.sleep(1)
            continue
        else:
            break
    else:
        raise Exception('Download failed')

def download_general_stats(user: str):
    download_file(
        pathlib.Path('general_stats.svg'),
        'https://github-readme-stats.vercel.app/api',
        params={
            'username': user,
            'theme': 'dark',
            'show_icons': 'true',
            'count_private': 'true',
            'include_all_commits': 'true',
        },
    )

def download_language_stats(user: str):
    download_file(
        pathlib.Path('language_stats.svg'),
        'https://github-readme-stats.vercel.app/api/top-langs',
        params={
            'username': user,
            'theme': 'dark',
            'show_icons': 'true',
            'count_private': 'true',
            'hide': 'html,css',
            'layout': 'compact',
        },
    )

@app.command()
def main(user: str = typer.Argument(..., help='GitHub username')):
    download_general_stats(user=user)
    download_language_stats(user=user)


if __name__ == '__main__':
    typer.run(main)