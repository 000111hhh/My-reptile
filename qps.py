import concurrent.futures
import requests
import time

# 设置线程数和总请求数量
num_threads = 100  # 线程数
total_requests = 10000  # 总请求数量
url = 'https://www.ruanyifeng.com/blog/'  # 待测试的网页地址

# 定义请求函数
count = 0


def make_request():
    global count
    response = requests.get(url)
    if count % 1000 == 0:
        print(response.status_code)
    count += 1


start_time = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(make_request) for _ in range(total_requests)]

concurrent.futures.wait(futures)

end_time = time.time()
total_time = end_time - start_time

qps = total_requests / total_time

print(f'QPS: {qps}')
print(total_requests, total_time)
