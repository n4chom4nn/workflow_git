import requests
import time

HTTP_RESPONSES = {
    200: ('OK', 'Request fulfilled, document follows'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    403: ('Forbidden', 'Request forbidden -- authorization will not help'),
    500: ('Internal Server Error', 'Server got itself in trouble')
}


def get_number_of_websites():
    while True:
        try:
            num_websites = int(input("Enter the number of websites you want to rate: "))
            if num_websites >= 3:
                return num_websites
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")


def get_multiple_url_inputs(num_websites):
    urls = []
    for i in range(num_websites):
        url = input(f"Please enter the URL of website {i + 1}: ")
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        urls.append(url)
    return urls


def measure_response_time(url):
    start_time = time.time()
    try:
        response = requests.get(url, timeout=10)
        response_time = time.time() - start_time

        status_code = response.status_code
        if status_code in HTTP_RESPONSES:
            print(f"Got response: {status_code} - {HTTP_RESPONSES[status_code][0]}")
        else:
            print(f"Got response: {status_code}")

        response.raise_for_status()
        return response_time
    except requests.exceptions.RequestException as e:
        print(f"Error for {url}: {str(e)}")
        return None


def main():
    num_websites = get_number_of_websites()
    urls = get_multiple_url_inputs(num_websites)

    response_times = []
    for url in urls:
        response_time = measure_response_time(url)
        if response_time is not None:
            response_times.append((url, response_time))

    if not response_times:
        print("No successful responses received.")
        return

    sorted_response_times = sorted(response_times, key=lambda x: x[1])
    top_3 = sorted_response_times[:3]

    print("\nTop 3 speed ranking:")
    for i, (url, time) in enumerate(top_3, 1):
        print(f"{i}. {url} - {time:.4f} seconds")

    average_speed = sum(time for _, time in response_times) / len(response_times)
    print(f"\nAverage speed: {average_speed:.4f} seconds")


if __name__ == "__main__":
    main()