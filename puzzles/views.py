import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Hint, Puzzle, Solve


# Serve media files
def media(request, file_path=None):
    with open(os.path.join(settings.MEDIA_ROOT, file_path), 'rb') as doc:
        response = HttpResponse(doc.read(), content_type='application/doc')
        response['Content-Disposition'] = 'filename=%s' % (file_path.split('/')[-1])
        return response


@login_required
def puzzle_tree(request):
    solves = Solve.objects.get(user=request.user)

    tree_nodes = []
    node_names = []

    for puzzle in Puzzle.objects.all():
        # If solved, or no parent (starting puzzle), or parent solved (yet to be solved)
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


@login_required
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
            hints = Hint.objects.filter(puzzle=puzzle)
            return render(request, "puzzles/puzzle_locked.html", {"puzzle": puzzle, "hints": hints})

    # If trying to unlock the puzzle through the form
    elif request.method == "POST":
        puzzle = Puzzle.objects.get(identifier=identifier)

        password = puzzle.password
        data = dict(request.POST)

        # Check if password is correct
        for i, c in enumerate(password):
            key = str(i + 1)

            # If a single character is wrong
            if data[key][0].lower() != c.lower():
                hints = Hint.objects.filter(puzzle=puzzle)
                return render(request, "puzzles/puzzle_locked.html", {"puzzle": puzzle, "hints": hints, "failed": True})

        # If password is correct, update
        solves = Solve.objects.get(user=request.user)
        solves.solved = solves.solved + [puzzle.identifier]
        solves.save()

        return render(request, "puzzles/puzzle_view.html", {"puzzle": puzzle})
