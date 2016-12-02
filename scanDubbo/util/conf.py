
npms_server_g = [
    ('10.110.92.151', 28880),
    ('10.110.92.166', 28880)

]

npms_server_h = [
    ('10.110.92.131', 28880),
    ('10.110.92.132', 28880)
]

npms_server_c=[
    ('10.110.92.130', 21880),
    ('10.110.92.153', 21880)
]

npms_point_server = [
    ('10.110.92.158', 20880),
    ('10.110.92.159', 20880)
]

servers = {
    "npms_server_g": npms_server_g,
    "npms_server_h": npms_server_h,
    "npms_server_c": npms_server_c,
    "npms_point_server": npms_point_server
}

service1 = [
    ("com.letv.shop.product.api.service.ISpuService", "getSpuBySpuNo")
]

serverList = {
    "host1": service1
}


