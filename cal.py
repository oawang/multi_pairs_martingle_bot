# package main

# import "fmt"

def main():
    target_amount = 17000  # USDT的总数
    iterations = 6  # 总共加仓次数
    increment_factor = 1.3  # 每次加仓的乘数因子
    initial_base = target_amount  # 初始基数设为目标总数

    sum = 0 # USDT的总数
    initial_base = 1000
    for i in range(iterations):
        sum += initial_base * (increment_factor ** (iterations - i))

    print(f"基数为：{initial_base}时， 需要投入的总数是: {sum}")


if __name__ == '__main__':
    main()
    print(-(0.8 - 1) > 0.1)

