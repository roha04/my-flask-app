from app.algorithms.salary import salary_benchmark
from app.algorithms.types import JobSalary


def test_salary_benchmark_percentile_for_mid_range():
    jobs = [
        JobSalary(salary_min=80000, salary_max=100000),
        JobSalary(salary_min=90000, salary_max=110000),
        JobSalary(salary_min=100000, salary_max=120000),
        JobSalary(salary_min=110000, salary_max=130000),
    ]
    result = salary_benchmark(105000, jobs)
    assert result["count"] == 4
    assert result["median"] == 105000.0
    assert 0.4 <= result["percentile"] <= 0.75


def test_empty_job_list_returns_null_stats():
    result = salary_benchmark(100000, [])
    assert result["count"] == 0
    assert result["percentile"] is None


def test_uses_single_sided_salary_when_max_missing():
    jobs = [JobSalary(salary_min=100000, salary_max=None)]
    result = salary_benchmark(100000, jobs)
    assert result["count"] == 1
    assert result["percentile"] == 1.0


def test_low_salary_has_low_percentile():
    jobs = [
        JobSalary(salary_min=50000, salary_max=60000),
        JobSalary(salary_min=90000, salary_max=100000),
        JobSalary(salary_min=110000, salary_max=120000),
    ]
    result = salary_benchmark(55000, jobs)
    assert result["percentile"] <= 0.34
