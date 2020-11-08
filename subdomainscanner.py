import requests
from threading import Thread
from queue import Queue

q = Queue()

def scan_subdomains(domain):
    global q
    while True:
        # get the subdomain from the queue
        subdomain = q.get()
        # scan the subdomain
        url = f"http://{subdomain}.{domain}"
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            print("[+] Discovered subdomain:", url)

        # we're done with scanning that subdomain
        q.task_done()


def main(domain, n_threads, subdomains):
    global q

    # fill the queue with all the subdomains
    for subdomain in subdomains:
        q.put(subdomain)

    for t in range(n_threads):
        # start all threads
        worker = Thread(target=scan_subdomains, args=(domain,))
        # daemon thread means a thread that will end when the main thread ends
        worker.daemon = True
        worker.start()


if __name__ == "__main__":
    print(""" __       _         _                       _                                             
/ _\_   _| |__   __| | ___  _ __ ___   __ _(_)_ __    ___  ___ __ _ _ __  _ __   ___ _ __ 
\ \| | | | '_ \ / _` |/ _ \| '_ ` _ \ / _` | | '_ \  / __|/ __/ _` | '_ \| '_ \ / _ \ '__|
_\ \ |_| | |_) | (_| | (_) | | | | | | (_| | | | | | \__ \ (_| (_| | | | | | | |  __/ |   
\__/\__,_|_.__/ \__,_|\___/|_| |_| |_|\__,_|_|_| |_| |___/\___\__,_|_| |_|_| |_|\___|_|   
                                                                                          """)
    domain = input("Enter Domain:")
    wordlist = "subdomains.txt"
    num_threads = 10

    main(domain=domain, n_threads=num_threads, subdomains=open(wordlist).read().splitlines())
    q.join()
    
    