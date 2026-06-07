from statistics import median

from app.algorithms.types import JobSalary


def _salary_midpoint(job: JobSalary) -> float | None:
    if job.salary_min is not None and job.salary_max is not None:
        return (job.salary_min + job.salary_max) / 2
    if job.salary_min is not None:
        return float(job.salary_min)
    if job.salary_max is not None:
        return float(job.salary_max)
    return None


def _percentile_rank(value: float, values: list[float]) -> float:
    if not values:
        return 0.0
    below_or_equal = sum(1 for item in values if item <= value)
    return below_or_equal / len(values)


def salary_benchmark(salary: float, job_list: list[JobSalary]) -> dict:
    """Compute salary percentile and distribution stats against stored jobs."""
    midpoints = sorted(mid for job in job_list if (mid := _salary_midpoint(job)) is not None)
    count = len(midpoints)
    if count == 0:
        return {
            "percentile": None,
            "median": None,
            "p25": None,
            "p75": None,
            "count": 0,
        }

    p25_index = max(0, int(count * 0.25) - 1)
    p75_index = min(count - 1, int(count * 0.75))
    return {
        "percentile": round(_percentile_rank(salary, midpoints), 4),
        "median": median(midpoints),
        "p25": midpoints[p25_index],
        "p75": midpoints[p75_index],
        "count": count,
    }
