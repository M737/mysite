from django.shortcuts import render

# Create your views here.
def grid_system(request):
    context = {}
    if request.method == 'POST':
        W = get_or_replace(request.POST, 'W', 0)
        n = get_or_replace(request.POST, 'n', 0)
        a = get_or_replace(request.POST, 'a', 0)
        i = get_or_replace(request.POST, 'i', 0)
        l = get_or_replace(request.POST, 'l', 0)

        context['items'] = run_with_param(W, n, a, i, l)

        return render(request, 'doudou/grid_system.html', context)
    return render(request, 'doudou/grid_system.html')


def formula(n, a, i ,l, W):
    return n*(a+i)- i + 2 * l == W

def even(num):
    return int(num) + 1 if int(num) % 2 else int(num)

def odd(num):
    return int(num)  if int(num) % 2 else int(num) + 1


def grid_with_width(request, width):
    context = {}
    context['items'] = run_with_param(width, 0, 0, 0, 0)
    return render(request, 'doudou/grid_system.html', context)


def run_with_param(W, n, a, i, l):
    items = []
    if not W:
        return []
    N = [n] if n else range(20, 31, 2)
    A = [a] if a else range(even(0.02*W), odd(0.03*W), 2)
    I = [i] if i else range(even(0.005*W), odd(0.015*W), 2)
    L = [l] if l else range(even(0.125*W), odd(0.25*W))
    for n in N:
        for a in A:
            for i in I:
                for l in L:
                    if formula(n, a, i, l, W):
                        item = {}
                        item['n'] = n
                        item['a'] = a
                        item['i'] = i
                        item['l'] = l
                        items.append(item)
    return items


def get_or_replace(item, key, num):
    try:
        values = int(item[key])
    except:
        values = num
    return values








