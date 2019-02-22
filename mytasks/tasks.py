import time

import dramatiq

from .utils import (check_if_odd, get_big_random_list, get_a_little_bit_bigger)


@dramatiq.actor(max_retries=0, max_age=3600000, time_limit=6000, store_results=True, result_ttl=6000000)
def not_even(x):
    time.sleep(5)
    if check_if_odd(x):
        raise Exception("!!! Something goes wrong...")
    else:
        return x


@dramatiq.actor(max_retries=5, max_age=3600)
def print_result(message_data, result):
    print(f"The result of message {message_data['message_id']} was {result}.")


@dramatiq.actor(max_retries=5, max_age=3600)
def print_error(message_data, exception_data):
    print(f"Message {message_data['message_id']} failed:")
    print(f"  * type: {exception_data['type']}")
    print(f"  * message: {exception_data['message']!r}")


@dramatiq.actor(store_results=True)
def find_smallest_in_small_array(data):
    sorted_list = sorted(data)
    return sorted_list[0]


@dramatiq.actor(max_retries=0, max_age=300000, store_results=True)
def find_smallest_in_big_array(data):
    """
    Lets distribute calculations on different workers
    :param data:
    :return:
    """
    workers_count = 4
    task_list = []
    slice_start = 0
    slice_end = None
    len_per_worker = len(data) // workers_count
    for i in range(1, workers_count):
        slice_end = slice_start + len_per_worker
        task_list.append(find_smallest_in_small_array.message(data[slice_start:slice_end]))
        slice_start = slice_end
    task_list.append(find_smallest_in_small_array.message(data[slice_end:]))

    g = dramatiq.group(task_list).run()
    result = list(g.get_results(block=True))
    smallest = sorted(result)[0]
    return smallest


@dramatiq.actor(store_results=True)
def prepare_big_random_list():
    # It's bad idea to send big bunch of data to result backend (redis) as results... so this is here just for example
    return get_big_random_list()


@dramatiq.actor(max_retries=0, max_age=300000, store_results=True)
def make_smallest_a_bit_bigger(data):
    return get_a_little_bit_bigger(than=data)


@dramatiq.actor(max_retries=0, max_age=300000)
def find_something_in_something_and_make_some_improvements():
    pipe = dramatiq.pipeline([
        prepare_big_random_list.message(),
        find_smallest_in_big_array.message(),
        make_smallest_a_bit_bigger.message()
    ]).run()

    return pipe.get_result(block=True, timeout=200000)
