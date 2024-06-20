# Periodic Network Ping Tool

This was to prove to my ISP that their network sucks.  

Logs basic network stats to a mysql db.  
Simple enough to convert to any other db if you like.  
Originally logged to tsv file for import, but this became too unstable for log-term use.  

## Usage

`python main.py <db host> <db user> <db pass> <db name>`

The output to the console is in tsv format - originally to pipe to a file

## DB

```
CREATE TABLE `ping` (
  `pingtime` datetime NOT NULL,
  `packet_loss` float NOT NULL,
  `average_time` float NOT NULL,
  `max_time` float NOT NULL,
  `min_time` float NOT NULL,
  `dns_ip` varchar(100) DEFAULT NULL,
  `dns_time` float DEFAULT NULL,
  PRIMARY KEY (`pingtime`)
)
```

### Queries

### 10 Min Stats
This groups the raw data into 10min buckets
```
select concat(concat(date(pingtime), 'H'), concat(lpad(hour(pingtime), 2, '0'), concat(':',lpad(truncate(minute(pingtime), -1), 2, '0')))) as ping_time, 
max(packet_loss) as packet_loss, avg(average_time) as average_time, max(max_time) as max_time, min(min_time) as min_time, 
case when max(dns_ip) = 'not found' then 1 else 0 end as dns_fail, max(dns_time) as dns_time
from ping
group by ping_time
```

### Hourly Stats
This groups the raw data into hourly buckets
```
select concat(concat(date(pingtime), 'H'), concat(lpad(hour(pingtime), 2, '0'), ':00')) as ping_time, 
max(packet_loss) as packet_loss, avg(average_time) as average_time, max(max_time) as max_time, min(min_time) as min_time, 
case when max(dns_ip) = 'not found' then 1 else 0 end as dns_fail, max(dns_time) as dns_time
from ping
group by ping_time
```
