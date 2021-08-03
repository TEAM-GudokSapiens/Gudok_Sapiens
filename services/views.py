from django.shortcuts import render


def main(request):
    ctx = {"main": main}
    return render(request, 'services/main.html', context=ctx)
