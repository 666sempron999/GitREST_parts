# -*- coding: utf-8 -*-

from config import Configurator

import requests

from timeit import default_timer as timer


def getIssueCount(repository):
    """Данная фкнкция открытых и закрытых issues.
    Входные параметры:
    repository - репозиторий для поиска
    Выходные параметры:
    opened - котлличество открытых issues
    closed - колличество закрытых issues
    (opened + closed) - и открытые и закрытые

    """

    url = "https://api.github.com/search/issues?q=repo:" + repository\
        + "+state:open&sort=created&order=asc&page=1&per_page=100"

    r = requests.get(url).json()
    opened = int(r['total_count'])

    url = "https://api.github.com/search/issues?q=repo:" + repository\
        + "+state:closed&sort=created&order=asc&page=1&per_page=100"

    r = requests.get(url).json()
    closed = int(r['total_count'])

    return opened, closed


if __name__ == '__main__':

    print("Скрипт для анализа репозитория " + Configurator.REPO_NAME)

    print("Колличество открытых и закрытых issues")

    start = timer()

    opened, closed = getIssueCount(Configurator.REPO_NAME)
    print("Открырые issues -" + str(opened))
    print("Закрытые issues -" + str(closed))

    end = timer()
    print("Exec time -", end - start)
