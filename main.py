import argparse
import datetime
import threading
import time

import dns
import dns.resolver
import mysql.connector
from pythonping import ping

next_call = time.time()

dbuser = "none"
dbpass = "none"
dbhost = "none"
dbname = "none"


def insert_row(ping_time, packet_loss, average_time, max_time, min_time, dns_ip, dns_time):
    connection = None
    try:
        connection = mysql.connector.connect(user=dbuser, password=dbpass, host=dbhost, database=dbname)
        cursor = connection.cursor(buffered=True)
        params = {"pingtime": ping_time, "packet_loss": packet_loss, "average_time": average_time, "max_time": max_time,
                  "min_time": min_time, "dns_ip": dns_ip, "dns_time": dns_time}
        cursor.execute(
            "insert into ping (pingtime, packet_loss, average_time, max_time, min_time, dns_ip, dns_time) values "
            "(%(pingtime)s, %(packet_loss)s, %(average_time)s, %(max_time)s, %(min_time)s, %(dns_ip)s, %(dns_time)s); ",
            params)
        connection.commit()
    except Exception as e:
        print(str(e))
    finally:
        if connection is not None:
            connection.close()


def main():
    global next_call
    try:
        result = ping("8.8.8.8")

        time_start = datetime.datetime.now()
        dns_result = dns.resolver.resolve("www.google.com", 'A')
        time_dns = datetime.datetime.now() - time_start
        ip = "not found"
        try:
            ip = list(dns_result.response.answer[0].items.keys())[0].address
        except:
            pass

        print(f"{datetime.datetime.now()}\t{result.packet_loss}\t{result.rtt_avg_ms}\t{result.rtt_max_ms}\t"
              f"{result.rtt_min_ms}\t{ip}\t{time_dns.microseconds / 1000}")
        insert_row(datetime.datetime.now(), result.packet_loss, result.rtt_avg_ms, result.rtt_max_ms, result.rtt_min_ms,
                   ip, time_dns.microseconds / 1000)
    except Exception as e:
        print(e)

    next_call = next_call + 10
    threading.Timer(next_call - time.time(), main).start()


if __name__ == '__main__':
    print("time\tloss\tavg\tmax\tmin\tip\ttdns")
    parser = argparse.ArgumentParser(description="periodic ping")
    parser.add_argument('dbhost',
                        help='DB Host',
                        type=str)
    parser.add_argument('dbuser',
                        help='Db Username',
                        type=str)
    parser.add_argument('dbpass',
                        help='Db Password',
                        type=str)
    parser.add_argument('db',
                        help='Db Name',
                        type=str)

    args = parser.parse_args()

    dbhost = args.dbhost
    dbuser = args.dbuser
    dbpass = args.dbpass
    dbname = args.db

    main()
