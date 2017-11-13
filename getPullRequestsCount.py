# -*- coding: utf-8 -*-

from config import Configurator
from timeit import default_timer as timer

import requests


def getPullRequestsCount(repository):

    """Данная фкнкция открытых и закрытых pull request.
    Входные параметры:
    repository - репозиторий для поиска
    Выходные параметры:
    open_count - котлличество открытых issues
    close_count - колличество закрытых issues


    """

    open_count = 0
    close_count = 0
    page_number = 1

    url = "https://api.github.com/repos/" + repository + "/pulls?q=&page="\
        + str(page_number) + "&per_page=100&state=all"

    r = requests.get(url).json()

    while len(r) == 100:

        for param in range(0, len(r)):

            if str(r[param]["state"]) == "open":
                open_count += 1

            elif str(r[param]["state"]) == "closed":
                close_count += 1

        page_number += 1

        url = "https://api.github.com/repos/" + repository + "/pulls?q=&page="\
            + str(page_number) + "&per_page=100&state=all"

        r = requests.get(url).json()

    for param in range(0, len(r)):

        if str(r[param]["state"]) == "open":
            open_count += 1

        elif str(r[param]["state"]) == "closed":
            close_count += 1

    return open_count, close_count


if __name__ == '__main__':

    print("Скрипт для анализа репозитория " + Configurator.REPO_NAME)

    print("Количество​​ открытых​​ и​​ закрытых​​ pull​​ requests")

    start = timer()
    op, cl = getPullRequestsCount(Configurator.REPO_NAME)

    end = timer()
    print("Открырые pull requests -" + str(op))
    print("Закрытые pull requests -" + str(cl))

    print("Exec time -", end - start)
