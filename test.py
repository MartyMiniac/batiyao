import json
'''
f=open('test.json','w')
js=[
    {
        'name':'test1',
        'nickname':'nick1',
        'ip':'192.168.29.4'
    },
    {
        'name':'test2',
        'nickname':'nick2',
        'ip':'192.168.29.5'
    },
    {
        'name':'test3',
        'nickname':'nick3',
        'ip':'192.168.29.6'
    },
    {
        'name':'test4',
        'nickname':'nick4',
        'ip':'192.168.29.7'
    },
]
f.write(json.dumps(js, indent=4))
f.close()
'''
f=open('test.json','r')
js=json.load(f)
f.close()
arr={
        'name':'test5',
        'nickname': 'nick5',
        'ip':'192.168.29.8'
    }
js.append(arr)
print(js)
f=open('test.json','w')
f.write(json.dumps(js, indent=4))
f.close()