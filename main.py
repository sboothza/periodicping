import datetime, threading, time
from pythonping import ping
import mysql.connector

next_call = time.time()


def insert_row(ping_time, packet_loss, average_time, max_time, min_time):
    connection = None
    try:
        connection = mysql.connector.connect(user="root", password="or9asm1c", host="localhost", database="trace")
        cursor = connection.cursor(buffered=True)
        params = {"pingtime": ping_time, "packet_loss": packet_loss, "average_time": average_time, "max_time": max_time,
                  "min_time": min_time}
        cursor.execute("insert into ping (pingtime, packet_loss, average_time, max_time, min_time) values "
                       "(%(pingtime)s, %(packet_loss)s, %(average_time)s, %(max_time)s, %(min_time)s); ", params)
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
        # print(str(result))

        print(
            f"{datetime.datetime.now()}\t{result.packet_loss}\t{result.rtt_avg_ms}\t{result.rtt_max_ms}\t{result.rtt_min_ms}")
        insert_row(datetime.datetime.now(), result.packet_loss, result.rtt_avg_ms, result.rtt_max_ms, result.rtt_min_ms)
    except Exception as e:
        print(e)

    next_call = next_call + 10
    threading.Timer(next_call - time.time(), main).start()


if __name__ == '__main__':
    print("time\tloss\tavg\tmax\tmin")
    main()
