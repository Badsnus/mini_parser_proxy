from time import sleep

from requests import get


def get_proxies(url: str) -> set[str]:
    response = get(url)
    if response.status_code == 200:
        return set(response.text.splitlines())
    print('Сервер не отвечает')
    return set()


def write_in_file(file_name: str, proxies_list: set) -> None:
    with open(file_name, 'a') as file:
        for proxy in proxies_list:
            file.write(proxy + '\n')


def main(url: str) -> None:
    file_name = input('Введите название файла: ')
    proxies = set()
    try:
        with open(file_name) as file:
            proxies = {*file.read().splitlines()}
    except FileNotFoundError:
        with open(file_name, 'w'):
            ...
    time_to_sleep = int(input('Сколько минут ждать между запросами: ')) * 60
    while True:
        proxies_got = get_proxies(url)
        if len(proxies_got) != 0:
            new_proxies = proxies_got - proxies
            write_in_file(file_name, new_proxies)
            print(f'Получил {len(new_proxies)} новых прокси. Ухожу в сон')
            sleep(time_to_sleep)


if __name__ == "__main__":
    url = 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt'
    main(url)