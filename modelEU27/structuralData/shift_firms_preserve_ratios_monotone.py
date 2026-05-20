import heapq
import math

def total_employees(firms_by_size, n_start=1):
    return sum((n_start + i) * c for i, c in enumerate(firms_by_size))


def shift_firms_preserve_ratios_monotone(
    firms_by_size,
    delta_employees,
    n_start=1,
    eps=1.0,
    monotone="auto",      # "auto", "increasing", "decreasing", "none"
    max_steps=None,
    refresh_window=2
):
    """
    Sposta imprese tra classi adiacenti per ottenere delta_employees (approssimato),
    preservando:
      - numero totale imprese (solo spostamenti)
      - monotonicità (se richiesta)
      - rapporti adiacenti f[i+1]/f[i] il più possibile (minimizzazione greedy della variazione
        dei log-rapporti rispetto all'originale)

    Obiettivo: minimizzare sum_i ( log((f'_{i+1}+eps)/(f'_i+eps)) - log((f_{i+1}+eps)/(f_i+eps)) )^2
    """
    f0 = list(firms_by_size)
    f = f0[:]
    N = len(f)

    requested = int(delta_employees)
    if N <= 1 or requested == 0:
        return f, 0, {
            "requested_delta": requested,
            "achieved_delta": 0,
            "monotone_mode": "none",
            "total_firms_before": sum(f0),
            "total_firms_after": sum(f),
            "total_employees_before": total_employees(f0, n_start=n_start),
            "total_employees_after": total_employees(f, n_start=n_start),
        }

    # monotonicità: auto-detect se richiesto
    def is_non_decreasing(a): return all(a[i] <= a[i+1] for i in range(len(a)-1))
    def is_non_increasing(a): return all(a[i] >= a[i+1] for i in range(len(a)-1))

    if monotone == "auto":
        if is_non_decreasing(f0):
            monotone_mode = "increasing"
        elif is_non_increasing(f0):
            monotone_mode = "decreasing"
        else:
            monotone_mode = "none"
    else:
        monotone_mode = monotone

    if monotone_mode not in ("increasing", "decreasing", "none"):
        raise ValueError("monotone must be 'auto', 'increasing', 'decreasing', or 'none'")

    # log-ratio base (target) dalla distribuzione originale
    base_lr = [math.log(f0[i+1] + eps) - math.log(f0[i] + eps) for i in range(N-1)]

    def local_cost_at(i, arr):
        lr = math.log(arr[i+1] + eps) - math.log(arr[i] + eps)
        d = lr - base_lr[i]
        return d * d

    def local_cost_sum(i_from, i_to, arr):
        a = max(0, i_from)
        b = min(N - 2, i_to)
        s = 0.0
        for i in range(a, b + 1):
            s += local_cost_at(i, arr)
        return s

    # monotonic feasibility checks for a unit move on edge k between k and k+1
    def feasible_right(k):
        # move 1 firm: k -> k+1  (f[k]--, f[k+1]++)
        if f[k] <= 0:
            return False
        if monotone_mode == "none":
            return True

        a = f[k] - 1
        b = f[k+1] + 1

        if monotone_mode == "increasing":
            if k-1 >= 0 and f[k-1] > a:      # f[k-1] <= new f[k]
                return False
            if a > b:                         # new f[k] <= new f[k+1]
                return False
            if k+2 < N and b > f[k+2]:        # new f[k+1] <= f[k+2]
                return False
            return True

        # decreasing
        if k-1 >= 0 and f[k-1] < a:          # f[k-1] >= new f[k]
            return False
        if a < b:                             # new f[k] >= new f[k+1]
            return False
        if k+2 < N and b < f[k+2]:            # new f[k+1] >= f[k+2]
            return False
        return True

    def feasible_left(k):
        # move 1 firm: (k+1) -> k  (f[k]++, f[k+1]--)
        if f[k+1] <= 0:
            return False
        if monotone_mode == "none":
            return True

        a = f[k] + 1
        b = f[k+1] - 1

        if monotone_mode == "increasing":
            if k-1 >= 0 and f[k-1] > a:
                return False
            if a > b:
                return False
            if k+2 < N and b > f[k+2]:
                return False
            return True

        # decreasing
        if k-1 >= 0 and f[k-1] < a:
            return False
        if a < b:
            return False
        if k+2 < N and b < f[k+2]:
            return False
        return True

    # marginal cost of a unit move (ratio-based objective), computed locally
    def inc_cost_right(k):
        if not feasible_right(k):
            return float("inf")
        before = local_cost_sum(k - 1, k + 1, f)
        ff = f[:]              # simple but safe; can be optimized if needed
        ff[k] -= 1
        ff[k+1] += 1
        after = local_cost_sum(k - 1, k + 1, ff)
        return after - before

    def inc_cost_left(k):
        if not feasible_left(k):
            return float("inf")
        before = local_cost_sum(k - 1, k + 1, f)
        ff = f[:]
        ff[k] += 1
        ff[k+1] -= 1
        after = local_cost_sum(k - 1, k + 1, ff)
        return after - before

    direction = "right" if requested > 0 else "left"
    remaining = abs(requested)
    achieved = 0
    steps = 0
    if max_steps is None:
        max_steps = remaining

    heap = []
    if direction == "right":
        for k in range(N-1):
            if feasible_right(k):
                heapq.heappush(heap, (inc_cost_right(k), k))
    else:
        for k in range(N-1):
            if feasible_left(k):
                heapq.heappush(heap, (inc_cost_left(k), k))

    while remaining > 0 and steps < max_steps and heap:
        cost, k = heapq.heappop(heap)

        if direction == "right":
            if not feasible_right(k):
                continue
            f[k] -= 1
            f[k+1] += 1
            achieved += 1
        else:
            if not feasible_left(k):
                continue
            f[k] += 1
            f[k+1] -= 1
            achieved -= 1

        remaining -= 1
        steps += 1

        # refresh local neighborhood of candidate moves
        lo = max(0, k - refresh_window)
        hi = min(N - 2, k + refresh_window)
        for kk in range(lo, hi + 1):
            if direction == "right":
                if feasible_right(kk):
                    heapq.heappush(heap, (inc_cost_right(kk), kk))
            else:
                if feasible_left(kk):
                    heapq.heappush(heap, (inc_cost_left(kk), kk))

    info = {
        "requested_delta": requested,
        "achieved_delta": achieved,
        "steps": steps,
        "direction": direction,
        "monotone_mode": monotone_mode,
        "eps": eps,
        "total_firms_before": sum(f0),
        "total_firms_after": sum(f),
        "total_employees_before": total_employees(f0, n_start=n_start),
        "total_employees_after": total_employees(f, n_start=n_start),
    }
    return f, achieved, info