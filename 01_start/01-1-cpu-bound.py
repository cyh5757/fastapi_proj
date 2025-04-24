def cpu_bound_task(number: int) -> int:
    """CPU 집약적인 작업을 수행하는 함수입니다.

    Args:
        number (int): 계산할 범위의 최대값

    Returns:
        int: 계산된 결과값
    """
    total = 1
    arrange = range(1, number + 1)
    for i in arrange:
        for j in arrange:
            for k in arrange:
                total *= i * j * k
    return total


if __name__ == "__main__":
    result = cpu_bound_task(10)
    print(result)
