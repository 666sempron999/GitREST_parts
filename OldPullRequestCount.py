# -*- coding: utf-8 -*-

from config import Configurator
from datetime import datetime

import requests
from timeit import default_timer as timer


def is_old(created_at, closed_at, daysCount):
    """
    Данная функция проверяет параметр на старость.
    Параметр считается старым, если он не закрывается​ в ​течение​\
    daysCount дней.
    Входные параметры
    created_at
    closed_at
    daysCount
    Выходные параметры
    True or False в зависимости от старости параметра
    """
    cr_date = created_at.split("T")[0]
    cl_date = closed_at.split("T")[0]

    cr_date = datetime.strptime(cr_date, "%Y-%m-%d")
    cl_date = datetime.strptime(cl_date, "%Y-%m-%d")

    if (cl_date - cr_date).days > daysCount:
        return True
    else:
        return False


def old_pull_request_count(repository):
    """Данная функция позволяет получить колличество старых pull request.
    Pull request старый, если он не закрывается​ в ​течение​ ​30​ ​дней.
    Входные параметры:
    repository - репозиторий для поиска
    Выходные параметры:
    counterOldPull - колличество старых pull request
    """

    counter_old_pull = 0
    page_number = 1

    url = "https://api.github.com/repos/" + repository + "/pulls?q=&page="\
        + str(page_number) + "&per_page=100&state=all"

    r = requests.get(url).json()

    while len(r) == 100:

        for param in range(0, len(r)):

            created = str(r[param]["created_at"])
            closed = str(r[param]["closed_at"])

            if created == "None" or closed == "None":
                continue

            elif is_old(created, closed, 30):
                counter_old_pull += 1

        page_number += 1

        url = "https://api.github.com/repos/" + repository + "/pulls?q=&page="\
            + str(page_number) + "&per_page=100&state=all"

        r = requests.get(url).json()

        for param in range(0, len(r)):

            created = str(r[param]["created_at"])
            closed = str(r[param]["closed_at"])

            if created == "None" or closed == "None":
                continue

            elif is_old(created, closed, 30):
                counter_old_pull += 1

    return counter_old_pull


if __name__ == '__main__':

    print("Скрипт для анализа репозитория " + Configurator.REPO_NAME)

    print("Количество старых pull requests")

    start = timer()
    print("Старые (не закрытые более 30 дней)-" + str(old_pull_request_count(
            Configurator.REPO_NAME)))

    end = timer()
    print("Exec time -", end - start)
