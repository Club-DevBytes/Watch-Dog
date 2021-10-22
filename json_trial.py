import json
data=json.loads('{"document":[{"name":"asdff","number":"3","color":"#DC2626"},{"name":"dgag","number":"5","color":"#CA8A04"}],"page":[{"name":"asadf","number":"4","color":"#16A34A"}],"blob":[{"name":"asddg","number":"5","color":"#2563EB"}]}')
print(data)
print(len(data))
for doc,page,blob in zip(data['document'],data['page'],data['blob']):
    print(page)
    print(doc)
    print(blob)
