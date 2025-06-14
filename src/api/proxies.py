from multiprocessing import Pool
from tqdm import tqdm

from pandas import Series, read_csv, concat
from requests import get
from functools import partial

def check_proxy(proxy):
    try:
        res = get("http://example.com", proxies={"http": proxy}, timeout=3)
        if res.ok:
            return proxy
    except IOError:
        return None
    else:
        return None

def get_proxies():
    print("Retrieving proxies...")
    proxies = read_csv(
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        header=None,
    )
    df = (
        read_csv(
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
            sep="|",
            header=None,
        )
        .iloc[:, 0]
        .reset_index(drop=True)
    )
    proxies = (
        concat([proxies, df])
        .drop_duplicates()
        .reset_index(drop=True)
        .values.tolist()
    )
    proxies = [p for sublist in proxies for p in sublist]
    print(f"Found {len(proxies)} proxies. Checking proxies...")
    with Pool(250) as p:
        proxies_iterator = p.imap_unordered(partial(check_proxy), proxies)
        proxies = list(tqdm(proxies_iterator, total=len(proxies), unit='proxy', leave=False, desc='Checking proxies...'))
    proxies = Series(proxies).dropna().tolist()
    print(f"Found {len(proxies)} valid proxies. Returning proxies...")
    return proxies