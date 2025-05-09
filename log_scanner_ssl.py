import ipaddress

#QUESTA FUNZIONE SERVE PER:
# OTTENERE UNA SOTTOSTRINGA Y DA UNA STRINGA X
# E TRASFORMARE QUELLA STRINGA X NELLA STRINGA Z = X - Y
def get_substring_and_remove_it(data, fst_del, snd_del, off1 = 0, off2 = 0):
    if fst_del.__class__ == int:
        fst_del_index = fst_del + off1
    else:
        fst_del_index = data.find(fst_del) + off1

    if snd_del.__class__ == int:
        snd_del_index = snd_del + off2
    else:
        snd_del_index = data.find(snd_del, fst_del_index+1) + off2

    substring = data[fst_del_index:snd_del_index]

    return [substring, data[snd_del_index + 1:]]


class error_line:
    
    ip = None
    time = None
    method = None
    server = None
    uri = None
    uri_params = None
    http_version = None
    http_status_code = None
    content_length = None
    ua = None

    def __init__(self, raw_line):
        elabored_line = ""
        raw_line = self.get_ip(raw_line)
        raw_line = self.get_time(raw_line)
        raw_line = self.get_http_attributes(raw_line)
        raw_line = self.get_http_status_code(raw_line)
        raw_line = self.get_http_resource_length(raw_line)
        raw_line = self.get_server(raw_line)
        raw_line = self.get_ua(raw_line)

    def get_ip(self, data : str):
        datas = get_substring_and_remove_it(data, 0, " ", 0, 0)
        self.ip = ipaddress.ip_address(datas[0])
        return datas[1]

    def get_time(self, data : str):
        datas = get_substring_and_remove_it(data, "- -", "]", 5, 0)
        self.time = datas[0]
        return datas[1]
    
    def get_http_attributes(self, data : str):
        datas = get_substring_and_remove_it(data, '"', '"', 0, 0)
        attributes = datas[0].split(" ")
        self.method = attributes[0]
        self.uri = attributes[1]
        self.http_version = float(attributes[2].split("/")[1])
        return datas[1]
    
    def get_http_status_code(self, data : str):
        datas = get_substring_and_remove_it(data, 0, " ", 1, 0)
        self.http_status_code = int(datas[0])
        return datas[1]
    
    def get_http_resource_length(self, data : str):
        datas = get_substring_and_remove_it(data, 0, " ", 0, 0)
        self.content_length = int(datas[0])
        return datas[1]
    
    def get_server(self, data : str):
        datas = get_substring_and_remove_it(data, '"', '"', 1, 0)
        self.server = datas[0].strip()
        return datas[1]

    def get_ua(self, data : str):
        self.ua = data[1:len(data)]
        return ''
    
    def __str__(self):
        return str(self.__dict__)

#line = error_line('0.0.0.0 - - [02/Jan/2022:06:5:4 -0500] "GET / HTTP/1.1" 200 4000 "https://website.com/" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36; 360Spider"')