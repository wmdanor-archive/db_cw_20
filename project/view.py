
def view_message(*items):
    print(*items)


def view_query_runtime(interval):
    print('Query runtime: ', round(interval*1000, 2), 'ms', sep='')


def view_exception(err):
    print(err)


def view_boolean_result(result):
    if result:
        print('Success')
    else:
        print('Failure')


def view_dict(dictionary, level=0):
    print('\t'*level, end='')
    length = len(dictionary)
    i = 1
    for key, value in dictionary.items():
        if type(value) is list:
            print('')
            view_entity_list(value, key, '', level)
        else:
            print(key, ': ', value, ' | ' if i != length else '', sep='', end='')
        i += 1
    print('')


def view_entity_list(container, entity, action='Found', level=0):
    print('\t' * level, end='')
    if container is None and action == 'Found':
        print('Not found')
        return
    if container is None:
        print(entity, 's is None', sep='')
        return

    action_formatted = '' if len(action) == 0 else action + ' '
    if type(container) is not list:
        print(action_formatted, entity, ':', sep='')
        view_dict(container, level+1)
        return

    if len(container) == 1:
        print(action_formatted, entity, ':', sep='')
        view_dict(container[0], level+1)
        return

    print(action_formatted, entity, 's:', sep='')
    for item in container:
        view_dict(item, level+1)

