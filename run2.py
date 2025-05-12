import heapq
import sys
import collections





# Константы для символов ключей и дверей
keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]
wall = '#'
robot = '@'


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


def find_paths(start, data):
    """Поиск кратчайших путей между узлами с учетом дверей и ключей."""
    paths = {}
    visited = set()
    queue = collections.deque([(start, 0, set())])
    direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current, distance, doors = queue.popleft()
        x, y = current

        """Избегаем повторных посещений"""
        if current in visited:
            continue
        visited.add(current)

        """Проверка на наличие ключа в текущей позиции"""
        cell = data[x][y]
        if cell in keys_char and current != start:
            paths[current] = (distance, doors)

        """Исследование соседних клеток"""
        for dx, dy in direction:
            nx, ny = x + dx, y + dy

            """Проверка доступности клетки и обработка дверей"""
            if data[nx][ny] != wall:
                new_doors = set(doors)
                if data[nx][ny] in doors_char:
                    new_doors.add(data[nx][ny].lower())
                queue.append(((nx, ny), distance + 1, new_doors))

    return paths


def min_steps_to_collect_all_keys(data):
    """Основная функция для поиска минимального количества шагов сбора всех ключей."""

    graph = {}
    keys = {}
    robots = []
    node_coords = []

    """Поиск стартовых позиций и ключей на карте"""
    for x, row in enumerate(data):
        for y, cell in enumerate(row):
            if cell == robot:
                robots.append((x, y))
                node_coords.append((x, y))
            elif cell in keys_char:
                keys[cell] = (x, y)
                node_coords.append((x, y))

    """Построение графа доступных путей"""
    for n, node in enumerate(node_coords):
        graph[n] = find_paths(node, data)

    """Реализация алгоритма Дейкстры с приоритетной очередью"""
    heap = [(0, tuple(robots), set())]
    visited = set()

    while heap:
        steps, current_positions, collected_keys = heapq.heappop(heap)

        """Проверка и сохранение состояний"""
        state = (tuple(current_positions), frozenset(collected_keys))
        if state in visited:
            continue
        visited.add(state)

        """Проверка условия завершения"""
        if len(collected_keys) == len(keys):
            return steps

        """Обработка возможных перемещений для каждого робота"""
        for robot_index, pos in enumerate(current_positions):
            node_index = node_coords.index(pos)

            """Анализ доступных целей для текущего робота"""
            for target_pos, (dist, req_doors) in graph[node_index].items():
                target_cell = data[target_pos[0]][target_pos[1]]
                if (target_cell in keys_char and
                        target_cell not in collected_keys and
                        all(door in collected_keys for door in req_doors)):
                    """Обновление состояния при сборе нового ключа"""
                    new_positions = list(current_positions)
                    new_positions[robot_index] = target_pos
                    new_collected = set(collected_keys)
                    new_collected.add(target_cell)
                    heapq.heappush(heap,(steps + dist, tuple(new_positions), new_collected))

    return -1


def main():
    data = get_input()
    print(min_steps_to_collect_all_keys(data))


if __name__ == "__main__":
    main()
