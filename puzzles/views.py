from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Puzzle, Solve


def puzzle_tree(request):
    solves = Solve.objects.get(user=request.user)

    tree_nodes = []
    node_names = []

    for puzzle in Puzzle.objects.all():
        # If solved, or parent solved (yet to be solved), or no parent (starting puzzle)
        if puzzle.identifier in solves.solved or not puzzle.parent or puzzle.parent.identifier in solves.solved:
            node_names.append(f"P{puzzle.pk}")

            if puzzle.parent:
                tree_nodes.append(
                    f'const P{puzzle.pk} = {{parent: P{puzzle.parent.pk}, text: {{name:"{puzzle.name}"}}, link: {{href: "/journal/{puzzle.identifier}"}}}};')
            else:
                tree_nodes.append(
                    f'const P{puzzle.pk} = {{text: {{name:"{puzzle.name}"}}, link: {{href: "/journal/{puzzle.identifier}"}}}};')

    tree_nodes.append(f'const tree_config = [config, {", ".join(node_names)}];')

    node_code = "\n".join(tree_nodes)

    return render(request, "puzzles/puzzle_tree.html", {"node_code": node_code})


def puzzle_view(request, identifier: str):
    # If trying to load a page
    if request.method == "GET":
        puzzle = Puzzle.objects.get(identifier=identifier)
        solved = Solve.objects.get(user=request.user).solved

        if puzzle.identifier in solved:
            # If solved
            return render(request, "puzzles/puzzle_view.html", {"puzzle": puzzle})
        else:
            # If not solved
            return render(request, "puzzles/puzzle_locked.html", {"puzzle": puzzle})

    # If trying to unlock the puzzle through the form
    elif request.method == "POST":
        puzzle = Puzzle.objects.get(identifier=identifier)

        password = puzzle.password
        data = dict(request.POST)
        print(data)

        # Check if password is correct
        for i, c in enumerate(password):
            key = str(i + 1)

            # If a single character is wrong
            if data[key] != [c]:
                return render(request, "puzzles/puzzle_locked.html", {"puzzle": puzzle, "failed": True})

        # If password is correct, update
        solves = Solve.objects.get(user=request.user)
        solves.solved = solves.solved + [puzzle.identifier]
        solves.save()

        return render(request, "puzzles/puzzle_view.html", {"puzzle": puzzle})
