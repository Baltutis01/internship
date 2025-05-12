import json





def check_capacity(max_capacity: int, guests: list) -> bool:
    # Реализация алгоритма

    """ Создаем список с датой заселения/выезда и параметром заселения/выезда """
    booking_list = []
    for guest in guests:
        booking_list.append((guest["check-in"],1))
        booking_list.append((guest["check-out"],-1))

    """ Сортировка сначала пройдет по датам и так же в рамках одной даты вначале будет выезд, а затем заселении """
    booking_list.sort()

    """ Вычитаем свободное место при заселении, добавляем при освобождении номера, если кто-то не влез, то False """
    for booking in booking_list:
        max_capacity -= booking[1]
        if max_capacity < 0:
            return False
    return True


if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())


    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)


    result = check_capacity(max_capacity, guests)
    print(result)
