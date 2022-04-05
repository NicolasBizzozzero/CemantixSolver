from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable

import tqdm


def execute_map_threads(
    func: Callable, iterable: Iterable, max_workers: int = 200
) -> None:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(func, tqdm.tqdm(iterable))
