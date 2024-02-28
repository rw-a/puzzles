from django.shortcuts import render
from .models import Puzzle, Solve


def puzzle_tree(request):
    solves = Solve.objects.get(user=request.user)

    tree_nodes = []
    node_names = []

    for puzzle in Puzzle.objects.all():
        # If solved, or parent solved (yet to be solved), or no parent (starting puzzle)
        if puzzle.pk in solves.solved or puzzle.parent.pk in solves.solved or not puzzle.parent:
            node_names.append(f"P{puzzle.pk}")

            if puzzle.parent:
                tree_nodes.append(
                    f'const P{puzzle.pk} = {{parent: P{puzzle.parent.pk}, text: {{name:"{puzzle.name}"}}}};')
            else:
                tree_nodes.append(
                    f'const P{puzzle.pk} = {{text: {{name:"{puzzle.name}"}}}};')

    tree_nodes.append(f'const tree_config = [config, {", ".join(node_names)}];')

    node_code = "\n".join(tree_nodes)

    return render(request, "puzzles/puzzle_tree.html", {"node_code": node_code})
