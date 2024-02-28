from django.shortcuts import render


def puzzle_tree(request):
    return render(request, "puzzles/puzzle_tree.html")
