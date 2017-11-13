# -*- coding: utf-8 -*-

from config import Configurator
from datetime import datetime
import requests

from timeit import default_timer as timer


def is_old(created_at, closed_at, days_count):
    """Данная функция проверяет параметр на старость.
    Параметр считается старым, если не закрывается​ в ​течение​ days_count.
    Входные параметры
    created_at
    closed_at
    days_count
    Выходные параметры
    True or False в зависимости от старости параметра

    """
    cr_date = created_at.split("T")[0]
    cl_date = closed_at.split("T")[0]

    cr_date = datetime.strptime(cr_date, "%Y-%m-%d")
    cl_date = datetime.strptime(cl_date, "%Y-%m-%d")

    if (cl_date - cr_date).days > days_count:
        return True
    else:
        return False


def getOldIssues(repository):
    """Данная функция врзвращает Количество “старых” issues.
    Issue считается старым, если он не закрывается в течение​​ 14​​ дней.
    Входные параметры:
    repository - репозиторий для поиска
    Выходные параметры:
    old_issues_count - Количество старых issues

    """

    old_issues_count = 0

    opened_issues, closed_issues = getIssueCount(repository)

    pages = ((opened_issues + closed_issues) // 100) + 1  # Получение
    # колличества страниц исходя из колличества открытых и закрытых issues

    for i in range(1, (pages + 1)):
        url = "https://api.github.com/repos/" + repository +\
            "/issues?q=&page=" + str(i) + "&per_page=100&state=all"

        r = requests.get(url).json()

        for param in range(0, len(r)):
            created = str(r[param]["created_at"])
            closed = str(r[param]["closed_at"])

            if created == "None" or closed == "None":
                continue

            elif is_old(created, closed, 14):
                old_issues_count += 1

    return old_issues_count


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

    print("Колличество старых issues (не закрытых в течении 14 дней)")

    start = timer()

    print("Старые issues -" + str(getOldIssues(Configurator.REPO_NAME)))

    end = timer()
    print("Exec time -", end - start)
