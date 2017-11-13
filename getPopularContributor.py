# -*- coding: utf-8 -*-

from config import Configurator

import requests
import texttable as tt

from timeit import default_timer as timer


def print_table(logins, commits):
    """Функция по данным двум спискам строит консольную таблицу"""

    tab = tt.Texttable()
    x = [[]]
    for i in range(0, 30):
        x.append([i+1, logins[i], commits[i]])

    tab.add_rows(x)
    tab.set_cols_align(['r', 'r', 'r'])

    tab.header(['Место', 'Логин', 'Колличество коммитов'])

    print(tab.draw())


def get_popular_contributor(repository):
    """Данная функция возвращает 30 самых активных участников репозитория.
    Активность определяется по колличеству коммитов.
    Входные параметры:
    repository - репозиторий для поиска
    Выходные параметры:
    authors - список авторов коммитов
    commits - колличество коммитов каждого автора


    """

    authors = []
    commits = []

    url = "https://api.github.com/repos/" + repository + "/stats/contributors"
    r = requests.get(url).json()

    print(r)

    for i in range(0, len(r)):
        authors.append(str(r[i]["author"]["login"]))
        commits.append(int(r[i]["total"]))

    authors.reverse()
    commits.reverse()

    authors = authors[:30]
    commits = commits[:30]

    return authors, commits


if __name__ == '__main__':

    print("Скрипт для анализа репозитория " + Configurator.REPO_NAME)

    print("Самые активные участники")

    start = timer()

    logins, commits = get_popular_contributor(Configurator.REPO_NAME)

    end = timer()

    print_table(logins, commits)
    print("Exec time -", end - start)
