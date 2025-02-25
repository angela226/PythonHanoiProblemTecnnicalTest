def is_valid_move(disk, target_rod):
    """Check if the disk can be placed on the target rod."""
    if not target_rod:
        return True  # If the rod is empty, any disk can be placed
    top_disk = target_rod[-1]
    return disk[0] < top_disk[0] and disk[1] != top_disk[1]  # Smaller size & different color


def hanoi_with_colors(n, disks, source="A", target="C", auxiliary="B", rods=None, moves=None):
    if rods is None:
        rods = {"A": disks[:], "B": [], "C": []}  # Initial state of rods
    if moves is None:
        moves = []

    # Check if the initial disks violate the color constraint
    for i in range(len(disks) - 1):
        if disks[i][1] == disks[i + 1][1]:  # Two consecutive disks have the same color
            return -1

    # Base case: No disks to move
    if n == 0:
        return moves

    # Move n-1 disks from source to auxiliary using target as helper
    result = hanoi_with_colors(n - 1, disks[:-1], source, auxiliary, target, rods, moves)
    if result == -1:
        return -1  # Stop if an invalid move is detected

    # Get the disk to be moved
    disk = rods[source][-1]  # Top disk on the source rod

    # Check if the move is valid
    if not is_valid_move(disk, rods[target]):
        return -1  # Invalid move due to size or color constraint

    # Move the disk
    rods[source].pop()
    rods[target].append(disk)
    moves.append((disk[0], source, target))

    # Move n-1 disks from auxiliary to target using source as helper
    result = hanoi_with_colors(n - 1, disks[:-1], auxiliary, target, source, rods, moves)
    if result == -1:
        return -1  # Stop if an invalid move is detected

    return moves


# Example Input 1 (Valid Case)
n1 = 3
disks1 = [(3, "red"), (2, "blue"), (1, "green")]  # Valid case

# Example Input 2 (Invalid Case - Same color constraint)
n2 = 3
disks2 = [(3, "red"), (2, "blue"), (1, "red")]  # Should return -1

# Running the function for both examples
result1 = hanoi_with_colors(n1, disks1)
result2 = hanoi_with_colors(n2, disks2)

# Print the outputs
print(result1)  # Expected valid moves for Example Input 1
print(result2)  # Expected -1 for Example Input 2 (Impossible)
