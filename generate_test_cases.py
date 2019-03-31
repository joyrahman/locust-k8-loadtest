# usage:

#python generate_test_case.py <output_file>
#output_format 

#test_id, #duration, #rate, #connection, #zone, #interference_level, #cart,#catalogue,#shipping,#start_pos, #end_pos



'''
cart-db44db4b9-q54pf        1/1     Running     0          18d
catalogue-f4f7886b-t5drm    1/1     Running     0          18d
dispatch-566f964cbd-xrsjf   1/1     Running     0          18d
mongodb-6b45dd6dcc-rng5p    1/1     Running     0          18d
mysql-7dd8588fb5-qz6fv      1/1     Running     0          18d
payment-689b48b7d9-6785z    1/1     Running     0          18d
rabbitmq-b4c48cb79-cdmdl    1/1     Running     0          18d
ratings-6bbf8c588d-7qkhh    1/1     Running     0          18d
redis-7fbd75b76d-krskv      1/1     Running     0          18d
shipping-bd5b4b46f-n984m    1/1     Running     0          18d
user-69d787d68b-l8rmg       1/1     Running     0          18d
web-6f7c94568-h49r4         1/1     Running     0          18d
'''
import sys
from datetime import date 
import hashlib
duration = 300 #sec


def getClusterConfiguration(cntCart=1,cntCatalogue=1,cntShipping=1,cntPayment=1,cntRatings=1,cntUser=1,cntWeb=1):
    pods = {}
    pods['cart'] = cntCart
    pods['catalogue'] = cntCatalogue
    pods['shipping'] = cntShipping
    pods['payment'] = cntPayment
    pods['ratings'] = cntRatings
    pods['user'] = cntUser
    pods['web'] = cntWeb


    return pods

def getConfigHash(pods):
    result = 0
    for k in pods:
        result *= 10
        result += pods[k]
    
    return result 

# cart_pod = 1
# catalogue_pod = 1
# shipping_pod = 1
# payemnt_pod = 1
# ratings_pod = 1
# user_pod = 1
# web_pod = 1

start_position = 5
end_position = 35

output_file = "default_test_case.csv"
if len(sys.argv) >1 :
    output_file  = sys.argv[1] 





zones = ['red','green','blue']
interference_level = [0,2,4]
connections  = []
for i in range(50,550,50):
    connections.append(i)
#connections = [125,250,500,1000,2000,4000]
#rate = max(connections)//4


# variables - zone, interference_level, connection
with open(output_file,'w' )as f:
    f.write("#test_id/duration/rate/con/zone/i_level/{configuration}/start_position/end_position\n")
    for zone in zones:
        for i_level in interference_level:
            for con in connections:
                rate = con//4

                today = date.today()
                #config = "{}:{}:{}".format(cart_pod,catalogue_pod,shipping_pod)
                
                date_prefix = today.strftime("%b%d")

                
                configuration = getClusterConfiguration()
                test_id = "{}_{}_{}_{}_{}".format(date_prefix,zone,con,i_level,getConfigHash(configuration) )
                data = "{}/{}/{}/{}/{}/{}/{}/{}/{}\n".format(test_id,duration,rate,con,zone,i_level,configuration,start_position,end_position)
                f.write(data)








