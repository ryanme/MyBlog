#/usr/bin/env python3
#encoding:utf-8

from MyServer.app import ticketprice

from_station = '南京'
to_station = '乌鲁木齐'
time = '2018-01-02'
ticketprice.get_price(from_station, to_station, time)


