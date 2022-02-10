# David Wang
# Wang93
# 112844282
# Programming Assignment 1

import sys
from datetime import datetime
import dns.query
import dns.message

# Create an instance of dns.message
msg = dns.message
root_server = "198.41.0.4"


# Takes in domain name and creates a query
def make_query(target, types):
    query = msg.make_query(target, types)
    return query


# Sends query to the IP address server, returns a response
def send_query(request, address):
    return dns.query.udp(request, address)


# Gets A response
def get_response(ip):
    response = send_query(make_query(ip, "A"), root_server)
    while not response.answer:
        additional = response.additional
        if not additional:
            authority = response.authority
            values = str(authority[0]).split()
            if values[3] == "NS":
                response = send_query(make_query(values[4], "A"), root_server)
            while not response.answer:
                additional = response.additional
                for x in additional:
                    values = str(x).split()
                    quest = str(response.question[0]).split()
                    if values[3] == "A":
                        response = send_query(make_query(quest[0], "A"), values[4])
        else:
            for xi in additional:
                values = str(xi).split()
                if values[3] == "A":
                    response = send_query(make_query(ip, "A"), values[4])
    return response


# Calculates the Query time
domain = sys.argv[1]
start = datetime.now()
arr = get_response(domain)
question = arr.question
answer = arr.answer
if str(question[0]).split()[0][:-1] != domain:
    Response = send_query(make_query(domain, "A"), str(answer[0]).split()[4])
answerArr = str(answer[0]).split()
if answerArr[3] == "CNAME":
    val = get_response(answerArr[4])
    question = val.question
    answer = val.answer
query_time = datetime.now() - start
output = "QUESTION SECTION:\n" + str(question[0]) + "\n" + "ANSWER SECTION:\n"
for x in answer:
    output += str(x) + "\n"
# Records information of Answer into a String
date = datetime.today()
when = date.strftime('%A')[:3] + " " + date.strftime('%B')[:3] + " " + date.strftime('%d') + " " + \
       date.strftime('%H:%M:%S') + " " + "Eastern Standard Time" + " " + date.strftime("%Y")
output += "Query time: " + str(round(query_time.total_seconds() * 1000)) + " msec\n" + "WHEN: " + when
print(output)
