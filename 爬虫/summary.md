---
author: 于梦娇
---

## 爬虫第一周总结



1. 获取网页资源

`response = requests.get(url, headers=headers)`

`response.text`

2. 获取图片等二进制资源

`response.content`

3. 解析页面



| 网站名称 | 技术                                       |
| ---- | ---------------------------------------- |
| 猫眼   | 正则表达式,适用于能直接从源代码中看到信息的网站                 |
| 豆瓣   | xpath                                    |
| 蘑菇街  | ajax,首页找不到,要到商品详情页看,network中XHR,将json数据转换出来 |
| 美剧网站 | 连接点击不了,url使用script渲染出来的,用正则表达式进行匹配       |
| 虾米音乐 | selenium                                 |
| 京东   | selenium                                 |



猫眼-正则表达式

```python
pattern = re.compile('<p class="x">(.*?)</p>', re.S)
# html 是传进来的参数,就是response.text返回的结果
items = re.findall(pattern, html)
# 然后用列表套字典的形式保存数据,返回列表结果
return result_list
```



豆瓣-xpath

```
def parse_page(html):
	etree_html = etree.HTML(html)
	# 匹配所有节点
	result = etree_html.xpath('//*')
	# 匹配所有子节点 //a 文本获取 text()
	result = etree_html.xpath('//a/text()')
	# 查找元素子节点 /
	result = etree_html.xpath('//div/p')
	# 父节点 ..
	result = etree_html.xpath('//span[@class="pubtime"]/../span/a/text()')
	# 属性匹配 [@class="xxx"]
	# 属性获取 @href

```



4. 保存图片

```python
def save_img():
	# 从解析的函数返回的列表数据中拿到图片的url,再经过response.content获取二进制资源
	# 进行保存
	for item in result_list:
		url = item['picture_url']
		content = get_resource(url)
		with open ('./image/文件名', 'wb') as f:
			f.write(content)
```

5. 保存成json数据

```python
# json.dumps将dict转成str
content = json.dumps(result_list, ensure_ascii=False)
with open ('./json/文件名', 'w', encoding='utf-8') as f:
    f.write(content)
```

6. 保存到数据库

```python
import pymysql

# 连接数据库
def get_connection():
	host = '127.0.0.1'
	port = 3306
	user = 'root'
	password = '123456'
	database = 'maoyan_db'
	db = pymysql.connect(host, user, password, database, charset='utf8', port=port)
	return db
	

# 获取数据库游标
def get_cursor(db):
	cursor = db.cursor()
	return cursor
	

# 关闭数据库连接
def close_db(db):
	db.close()
	
	
# 插入数据
def insert_record(db, cursor, result_dict):
	sql = "insert into maoyan (actor, movie, rate, releasetime, score, cover) values ('%s', '%s', '%s', '%s', '%s', '%s')" % (result_dict['actor'], result_dict['movie'], result_dict['rate'], result_dict['time'], result_dict['score'], result_dict['picture'])
    print(sql)
    cursor.execute(sql)
    db.commit()
	
```



