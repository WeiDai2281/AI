assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    cols = "123456789"
    rows = "ABCDEFGHI"
    boxes = cross(rows, cols)
    rowunit = [cross(r,cols) for r in rows]
    colunit = [cross(rows, c) for c in cols]
    squares = [cross(rs, cs) for rs in ("ABC", "DEF", "GHI") for cs in ("123", "456", "789")]
    diagnal1 = [[rows[s] + cols[v] for s in range(9) for v in range(9) if s == v]]
    diagnal2 = [[rows[s] + cols[v] for s in range(9) for v in range(9) if s == 8 - v]]
    unitlist = rowunit + colunit + squares + diagnal1 + diagnal2
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    twins = {}
    visited = set()
    for cell in boxes:
        if len(values[cell]) != 2 or cell in visited: 
            continue;
        for peer in peers[cell]:
            if values[cell] == values[peer]:
                twins[(cell, peer)] = values[peer]
                visited.add(peer)
                
    for (twin1, twin2) in twins:
        for peer in peers[twin1] & peers[twin2]:
            values = assign_value(values, peer, values[peer].replace(twins[(twin1, twin2)][0], ''))
            values = assign_value(values, peer, values[peer].replace(twins[(twin1, twin2)][1], ''))
                
    return values
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+v for s in A for v in B]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    cols = "123456789"
    rows = "ABCDEFGHI"
    boxes = cross(rows, cols)
    dic = dict(zip(boxes, grid))
    for cell in boxes:
        if dic[cell] == '.':
            dic[cell] = "123456789"
    return dic

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if not values:
        return False
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    cols = "123456789"
    rows = "ABCDEFGHI"
    boxes = cross(rows, cols)
    rowunit = [cross(r,cols) for r in rows]
    colunit = [cross(rows, c) for c in cols]
    squares = [cross(rs, cs) for rs in ("ABC", "DEF", "GHI") for cs in ("123", "456", "789")]
    diagnal1 = [[rows[s] + cols[v] for s in range(9) for v in range(9) if s == v]]
    diagnal2 = [[rows[s] + cols[v] for s in range(9) for v in range(9) if s == 8 - v]]
    unitlist = rowunit + colunit + squares + diagnal1 + diagnal2
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    for cell in values:
        if len(values[cell]) == 1:
            digit = values[cell]
            for peer in peers[cell]:
                assign_value(values, peer, values[peer].replace(digit, ''))
    return values

def only_choice(values):
    cols = "123456789"
    rows = "ABCDEFGHI"
    boxes = cross(rows, cols)
    rowunit = [cross(r,cols) for r in rows]
    colunit = [cross(rows, c) for c in cols]
    squares = [cross(rs, cs) for rs in ("ABC", "DEF", "GHI") for cs in ("123", "456", "789")]
    diagnal1 = [[rows[s] + cols[v] for s in range(9) for v in range(9) if s == v]]
    diagnal2 = [[rows[s] + cols[v] for s in range(9) for v in range(9) if s == 8 - v]]
    unitlist = rowunit + colunit + squares + diagnal1 + diagnal2
    for unit in unitlist:
        for digit in "123456789":
            dlist = []
            for element in unit:
                if digit in values[element]:
                    dlist.append(element)
            if len(dlist) == 1:
                assign_value(values, dlist[0], digit)
    return values
                
    
def reduce_puzzle(values):
    cols = "123456789"
    rows = "ABCDEFGHI"
    boxes = cross(rows, cols)
    solved_values = sum(len(values[box]) for box in boxes)
    stalled = False
    while not stalled:
        solved_values_before = sum(len(values[box]) for box in boxes)
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = sum(len(values[box]) for box in boxes)
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
        
    return values

def search(values):
    cols = "123456789"
    rows = "ABCDEFGHI"
    boxes = cross(rows, cols)
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[cell]) == 1 for cell in boxes):
        return values
    prob = 9
    for cell in boxes:
        if len(values[cell]) == 1: continue
        if len(values[cell]) < prob:
            fewest = cell
            prob = len(values[fewest])
    
    for test in values[fewest]:
        temp = values.copy()
        temp[fewest] = test
        attempt = search(temp)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values
    

if __name__ == '__main__':
    cols = "123456789"
    rows = "ABCDEFGHI"
    boxes = cross(rows, cols)
    rowunit = [cross(r,cols) for r in rows]
    colunit = [cross(rows, c) for c in cols]
    squares = [cross(rs, cs) for rs in ("ABC", "DEF", "GHI") for cs in ("123", "456", "789")]
    diagnal1 = [[rows[s] + cols[v] for s in range(9) for v in range(9) if s == v]]
    diagnal2 = [[rows[s] + cols[v] for s in range(9) for v in range(9) if s == 8 - v]]
    unitlist = rowunit + colunit + squares + diagnal1 + diagnal2
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    diag_sudoku_grid = "1......2.....9.5...............8...4.........9..7123...........3....4.....936.4.."
    display(solve(diag_sudoku_grid))

#     try:
#         from visualize import visualize_assignments
#         visualize_assignments(assignments)

#     except SystemExit:
#         pass
#     except:
#         print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')






