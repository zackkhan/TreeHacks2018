def split_string(s, k):
    res_list = []
    count = 0
    curr_string = ""
    sentences = s.split('.')
    for word in sentences:
        if (count == len(sentences) or count % k == 0):
            if curr_string != "":
                res_list.append(curr_string)
            curr_string = ""
        curr_string += word + "."
        count += 1
    return res_list
s = "Hello. My name is Zack. I Like pizza. I also like apples. Blha blha bl hal. yo whats goood. I am at treehacks."
x = split_string(s, 5)
print(x)
