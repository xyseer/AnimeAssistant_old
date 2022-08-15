# -*- coding:utf-8 -*-
import flask
from flask import Flask, request, render_template, redirect

import schedule_work
from GLOBAL_DEFINE import *
from databaseTool import ProcessingNameTable, ProcessingSubscriptionTable, ProcessingMetaDataTable, \
    ProcessingDownloadTable

app = Flask(__name__, static_folder='static')


@app.route("/user", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # username = request.form['username']使用request获取数据
        # password = request.form['password']
        # 也可以使用类实例里的表单方法来获取相应的数据
        # validate来验证输入的表单数据是否有效
        pass
    return render_template("form1.html")


@app.route("/")
def homepage():
    html = '''<!DOCTYPE html >
<html >
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xy-nas-tools</title>
<link href="static/css.css" rel="stylesheet" type="text/css" />
<style type="text/css">

</style>
</head>

<body>
<div class="box">
<table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td><h1>xy-nas-tool</h1></td>
    <td width="100" align="center"><a href="./">主页</a></td>
    <td width="100" align="center"><a href="./all">在追番剧</a></td>
    <td width="100" align="center"><a href="./setting">设置</a></td>
    <td width="100" align="center"><a href="./log">查看日志</a></td>
    <td width="100" align="center"><a href="./about">关于</a></td>
  </tr>
</table>
<table width=80% border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <th width=16%>图片</th>
  <th width=14%>名称</th>
  <th width=30%>简介</th>
  <th width=10%>下次更新时间</th>
  <th width="5%">下次更新集数</th>
  <th width=25%>操作</th>
</table>
'''
    db = AnimeDataBase(DB_PATH)
    for item in ProcessingSubscriptionTable(db).getSearchResult():
        if ProcessingSubscriptionTable(db).getSearchResult(table_id=int(item.get("id")))[0].get("nextUpdateEP", 0) > \
                ProcessingSubscriptionTable(db).getSearchResult(table_id=int(item.get("id")))[0].get("totalEpisodes",
                                                                                                     -1):
            continue
        if ProcessingNameTable(db).isInNameTable(table_id=int(item.get("id"))):
            id = int(item.get("id"))
            name = ProcessingNameTable(db).getSearchResult(table_id=id)[0].get("name", "")
            metadata = ProcessingMetaDataTable(db).getSearchResult(table_id=id)[0].get("info", "")
            img = ProcessingMetaDataTable(db).getSearchResult(table_id=id)[0].get("img", "")
            nextTime = ProcessingSubscriptionTable(db).getSearchResult(table_id=id)[0].get("nextUpdateTime").strftime(
                HTML_TIME_FORMAT)
            nextEP = ProcessingSubscriptionTable(db).getSearchResult(table_id=id)[0].get("nextUpdateEP", 0)
            html += f'''
                <br>
<table width=80% height="200" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr>
  <td width=16%><img src="{img}" width=100%></td>
  <td width=14% align="center">{name}</td>
  <td width=30% align="center">{metadata}</td>
  <td width=10% align="center">{nextTime}</td>
  <td width="5%" align="center">{nextEP}</td>
    <td width=25% align="center"><a href="detail?id={id}"><button class="button1">详情</button></a>
    <a href="update?id={id}"><button class="button2">立即更新</button></a></td>
  </tr>
</table>
            '''
            continue
        html += '''
  <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td align=center><h4>xy-nas-tool V1.0.0.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
  </tr>
</table>
              </div>
</body>
</html>
        '''
    return html


@app.route('/all')
def animelist():
    html = '''<!DOCTYPE html >
<html >
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xy-nas-tools</title>
<link href="static/css.css" rel="stylesheet" type="text/css" />
<style type="text/css">

</style>
</head>

<body>
<div class="box">
<table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td><h1>xy-nas-tool</h1></td>
    <td width="100" align="center"><a href="./">主页</a></td>
    <td width="100" align="center"><a href="./all">在追番剧</a></td>
    <td width="100" align="center"><a href="./setting">设置</a></td>
    <td width="100" align="center"><a href="./log">查看日志</a></td>
    <td width="100" align="center"><a href="./about">关于</a></td>
  </tr>
</table>
<table width=80% border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <th width=16%>图片</th>
  <th width=14%>名称</th>
  <th width=30%>简介</th>
  <th width=10%>下次更新时间</th>
  <th width="5%">下次更新集数</th>
  <th width=25%>操作</th>
</table>
<br>
<table width=80% height="40px" align="center" cellpadding="1" cellspacing="0">
<tr><td align="center">
<a href="add"><button class="button_add">点此以新增剧集</button></a></td>
</tr>
</table>
'''
    db = AnimeDataBase(DB_PATH)
    for item in ProcessingSubscriptionTable(db).getSearchResult():
        if ProcessingNameTable(db).isInNameTable(table_id=int(item.get("id"))):
            id = int(item.get("id"))
            name = ProcessingNameTable(db).getSearchResult(table_id=id)[0].get("name", "")
            metadata = ProcessingMetaDataTable(db).getSearchResult(table_id=id)[0].get("info", "")
            img = ProcessingMetaDataTable(db).getSearchResult(table_id=id)[0].get("img", "")
            nextTime = ProcessingSubscriptionTable(db).getSearchResult(table_id=id)[0].get(
                "nextUpdateTime").strftime(
                HTML_TIME_FORMAT)
            nextEP = ProcessingSubscriptionTable(db).getSearchResult(table_id=id)[0].get("nextUpdateEP", 0)
            html += f'''
                <br>
<table width=80% height="200" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr>
  <td width=16%><img src="{img}" width=100%></td>
  <td width=14% align="center">{name}</td>
  <td width=30% align="center">{metadata}</td>
  <td width=10% align="center">{nextTime}</td>
  <td width="5%" align="center">{nextEP}</td>
    <td width=25% align="center"><a href="detail?id={id}"><button class="button1">详情</button></a>
    <a href="update?id={id}"><button class="button2">立即更新</button></a>
    <a href="modify?id={id}"><button class="button3">修改</button></a>
    </td>
  </tr>
</table>
            '''
            continue
        html += '''
  <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td align=center><h4>xy-nas-tool V1.0.0.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
  </tr>
</table>
              </div>
</body>
</html>
        '''
    return html


@app.route('/detail', methods=['GET'])
def detail():
    id = int(request.args["id"])
    db = AnimeDataBase(DB_PATH)
    sub_item = ProcessingSubscriptionTable(db).getSearchResult(table_id=id)[0]
    mt_item = ProcessingMetaDataTable(db).getSearchResult(table_id=id)[0]
    dl_item = ProcessingDownloadTable(db).getSearchResult(table_id=id)[0]
    name = ProcessingNameTable(db).getSearchResult(table_id=id)[0].get("name", "")
    metadata = mt_item.get("info", "")
    img = mt_item.get("img", "")
    nextTime = sub_item.get("nextUpdateTime", datetime.now()).strftime(HTML_TIME_FORMAT)
    nextEP = sub_item.get("nextUpdateEP", 0)
    lastTime = sub_item.get("lastUpdateTime", datetime.now()).strftime(HTML_TIME_FORMAT)
    lastEP = sub_item.get("lastUpdateEP", 0)
    startTime = sub_item.get("starttime", datetime.now()).strftime(HTML_TIME_FORMAT)
    totalEP = sub_item.get("totalEpisodes", 0)
    span = sub_item.get("span", 168)
    way = dl_item.get("downloadway", "None")
    source = dl_item.get("source", "")
    directory = dl_item.get("directory", "")
    filter_name = dl_item.get("filter", "default")
    db.__del__()
    html = f'''
    <!DOCTYPE html >
<html >
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xy-nas-tools</title>
<link href="static/css.css" rel="stylesheet" type="text/css" />
<style type="text/css">

</style>
</head>

<body>
<div class="box">
<table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td><h1>xy-nas-tool</h1></td>
    <td width="100" align="center"><a href="./">主页</a></td>
    <td width="100" align="center"><a href="./all">在追番剧</a></td>
    <td width="100" align="center"><a href="./setting">设置</a></td>
    <td width="100" align="center"><a href="./log">查看日志</a></td>
    <td width="100" align="center"><a href="./about">关于</a></td>
  </tr>
</table>
<table width=80% border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr>
    <td rowspan="2" width=20% align="center"><img src="{img}" height="300" width=100%></td>
    <td colspan="3" width="80%" height=50 align="center">{name}</td>
  </tr>
  <tr>
    <td colspan="3" height="60%" align="center">{metadata}</td>
  </tr>
</table>
<table width=80% height="300" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr>
    <td width="25%" align="center">开播时间</td>
    <td width="25%" align="center">{startTime}</td>
    <td width="25%" align="center">总集数</td>
    <td width="25%" align="center">{totalEP}</td>
  </tr>
  <tr>
    <td width="25%" align="center">上次更新时间</td>
    <td width="25%" align="center">{lastTime}</td>
    <td width="25%" align="center">上次更新集数</td>
    <td width="25%" align="center">{lastEP}</td>
  </tr>
  <tr>
    <td width="25%" align="center">下次更新时间</td>
    <td width="25%" align="center">{nextTime}</td>
    <td width="25%" align="center">下次更新集数</td>
    <td width="25%" align="center">{nextEP}</td>
  </tr>
  <tr>
    <td width="25%" align="center">更新间隔</td>
    <td width="25%" align="center">{span} h</td>
    <td width="25%" align="center">更新方式</td>
    <td width="25%" align="center">{way}</td>
  </tr>
</table>
  <table width=80% height="200" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
    <tr>
    <td width="50%" align="center">下载来源</td>
    <td width="50%" align="center">{source}</td>
  </tr>
    <tr>
    <td width="50%" align="center">下载目录</td>
    <td width="50%" align="center">{directory}</td>
  </tr>
    </tr>
    <tr>
    <td width="50%" align="center">过滤条件</td>
    <td width="50%" align="center">{FILTER_DICTS.get(filter_name)}</td>
  </tr>
  </table>

  <table width="100%" height="80" border="0" cellpadding="0" cellspacing="0" class="buttons">
  <tr>
    <td  align="right">
      <button class="button2" onclick="javascript :history.back(-1);">返回</button>
    </td>
  </tr>
</table>

  <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td align=center><h4>xy-nas-tool V1.0.0.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
  </tr>
</table>

  </div>
</body>
</html>



    '''
    return html


@app.route("/update", methods=["GET"])
def update_imm():
    try:
        if int(request.args.get("id","0"))>0:
            schedule_work.run_time_up_work(schedule_work.SubscriptionItem(ProcessingSubscriptionTable(AnimeDataBase(DB_PATH)).getSearchResult(int(request.args.get("id","0")))[0]))
    except Exception as e:
        return f'''<script type="text/javascript">
                    alert("Error when update:{str(e)};history.back(-1);</script>'''
    finally:
        return f'''<script type="text/javascript">history.back(-1);</script>'''


@app.route("/add")
def add_item():
    try:
        db = AnimeDataBase(DB_PATH)
        new_id=ProcessingNameTable(db).getLastValidID()
        ProcessingNameTable(db).writeDB("在这里输入名称",new_id)
        ProcessingMetaDataTable(db).writeDB(new_id,"/static/default.jpg","在这里输入简介")
        ProcessingSubscriptionTable(db).writeDB(new_id,datetime.now(),0,datetime.now(),0,datetime.now(),0,168,"download")
        ProcessingDownloadTable(db).writeDB(new_id,"","","way_jackett","default")
        db.__del__()
        return redirect(f"modify?id={new_id}")
    except Exception as e:
        return f'''<script type="text/javascript">
                    alert("Error when update:{str(e)};history.back(-1);</script>'''



@app.route("/modify", methods=["GET"])
def modify():
    try:
        if int(request.args["id"]) > 0:
            id = int(request.args["id"])
            db = AnimeDataBase(DB_PATH)
            sub_item = ProcessingSubscriptionTable(db).getSearchResult(table_id=id)[0]
            mt_item = ProcessingMetaDataTable(db).getSearchResult(table_id=id)[0]
            dl_item = ProcessingDownloadTable(db).getSearchResult(table_id=id)[0]
            name = ProcessingNameTable(db).getSearchResult(table_id=id)[0].get("name", "")
            metadata = mt_item.get("info", "")
            img = mt_item.get("img", "")
            nextTime = sub_item.get("nextUpdateTime", datetime.now()).strftime(DB_TIME_FORMAT)
            nextEP = sub_item.get("nextUpdateEP", 0)
            lastTime = sub_item.get("lastUpdateTime", datetime.now()).strftime(DB_TIME_FORMAT)
            lastEP = sub_item.get("lastUpdateEP", 0)
            startTime = sub_item.get("starttime", datetime.now()).strftime(DB_TIME_FORMAT)
            totalEP = sub_item.get("totalEpisodes", 0)
            span = sub_item.get("span", 168)
            way = dl_item.get("downloadway", "None")
            source = dl_item.get("source", "")
            directory = dl_item.get("directory", "")
            filter_name = dl_item.get("filter", "default")
            db.__del__()

    except Exception as e:
        return ""

    html = f'''
        <!DOCTYPE html >
<html >
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xy-nas-tools</title>
<link href="static/css.css" rel="stylesheet" type="text/css" />
<style type="text/css">

</style>
</head>

<body>
<div class="box">

<table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td><h1>xy-nas-tool</h1></td>
    <td width="100" align="center"><a href="./">主页</a></td>
    <td width="100" align="center"><a href="./all">在追番剧</a></td>
    <td width="100" align="center"><a href="./setting">设置</a></td>
    <td width="100" align="center"><a href="./log">查看日志</a></td>
    <td width="100" align="center"><a href="./about">关于</a></td>
  </tr>
</table>
   <form action="/submit" method="post" enctype="multipart/form-data">
<table width=80% border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr>
    <td rowspan="2" width=20% align="center"><img src="{img}" id="image-preview" height="300" width=100%>
	<input type="file" id="file" name="img" accept="image/jpeg, image/png, image/jpg">
      <script type="text/javascript">
      ''' + '''
			let fileInput = document.getElementById('file');
			let preview = document.getElementById('image-preview');
			// 监听change事件:
			fileInput.addEventListener('change', function() {
				// 清除背景图片:
				preview.style.backgroundImage = '';
				let file = fileInput.files[0];
				if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
					alert('不是有效的图片文件!');
					return;
				}
				// 读取文件:
				let reader = new FileReader();
				reader.onload = function(e) {
					let data = e.target.result;
					preview.src = data
				};
				// 以DataURL的形式读取文件:
				reader.readAsDataURL(file);

			});
</script>
''' + f'''
</td>
    <td colspan="3" width="80%" height=50 align="center"><input type="text" value="{name}" class="text1" name="name"></td>
  </tr>
  <tr>
    <td colspan="3" height="60%" align="center"><textarea class="text1" name="meta">{metadata}</textarea></td>
  </tr>
</table>
<table width=80% height="300" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr>
    <td width="25%" align="center">开播时间</td>
    <td width="25%" align="center"><input align="center" type="datetime-local" value="{startTime}" class="text1" name="starttime"></td>
    <td width="25%" align="center">总集数</td>
    <td width="25%" align="center"><input type="number" value="{totalEP}" class="text1" name="totaleps"></td>
  </tr>
  <tr>
    <td width="25%" align="center">上次更新时间</td>
    <td width="25%" align="center"><input align="center" type="datetime-local" value="{lastTime}" class="text1" name="lasttime"></td>
    <td width="25%" align="center">上次更新集数</td>
    <td width="25%" align="center"><input type="number" value="{lastEP}" class="text1" name="lastep"></td>
  </tr>
  <tr>
    <td width="25%" align="center">下次更新时间</td>
    <td width="25%" align="center"><input align="center" type="datetime-local" value="{nextTime}" class="text1" name="nexttime"></td>
    <td width="25%" align="center">下次更新集数</td>
    <td width="25%" align="center"><input type="number" value="{nextEP}" class="text1" name="nextep"></td>
  </tr>
  <tr>
    <td width="25%" align="center">更新间隔</td>
    <td width="25%" align="center"><input type="number" width=80% value="{span}" class="span" name="span"> <label>小时</label></td>
    <td width="25%" align="center">更新方式</td>
    <td width="25%" align="center">
      <select class="text1" name="way">
        <option>way_jackett</option>
      </select>
    </td>
  </tr>
</table>
  <table width=80% height="200" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
    <tr>
    <td width="50%" align="center">下载来源</td>
    <td width="50%" align="center"><input type="text" value="{source}" class="text1" name="source"></td>
  </tr>
    <tr>
    <td width="50%" align="center">下载目录</td>
    <td width="50%" align="center"><input type="text" value="{directory}" class="text1" name="directory"></td>
  </tr>
    </tr>
    <tr>
    <td width="50%" align="center">过滤条件</td>
    <td width="50%" align="center">
      <select class="text1" name="filter">'''
    html += f"<option>{filter_name}</option>"
    for i in FILTER_DICTS.keys():
        if i != filter_name:
            html += f"<option>{i}</option>"
    html += f'''
      </select>
    </td>
    <input type="hidden" name="id" value="{id}">
  </tr>
  </table>

  <table width="100%" height="80" border="0" cellpadding="0" cellspacing="0" class="buttons">
  <tr>
    <td  align="right">
      <button class="button2" onclick="javascript :history.back(-1);" type="button">返回</button>
      <button class="button3" onclick="confirmDialog()" type="button">删除</button>
      <button class="button1" type="submit">提交</button>
      <script type="text/javascript">''' + '''
        function confirmDialog(){
			if(confirm("确认删除吗？")){
	    		top.location="./delete?id=1";
			}else{
			}
    	}
      </script>''' + f'''
    </td>
  </tr>
</table>

  <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td align=center><h4>xy-nas-tool V1.0.0.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
  </tr>
</table>
</form>
  </div>
</body>
</html>
    '''
    return html


@app.route("/submit", methods=["POST"])
def submit():
    try:
        if request.method == 'POST':
            id = request.form.get("id", "")
            name = request.form.get("name", "")
            starttime = request.form.get("starttime", "")
            meta = request.form.get("meta", "")
            totaleps = request.form.get("totaleps", "")
            lasttime = request.form.get("lasttime", "")
            lastep = request.form.get("lastep", "")
            nexttime = request.form.get("nexttime", "")
            nextep = request.form.get("nextep", "")
            span = request.form.get("span", "")
            source = request.form.get("source", "")
            directory = request.form.get("directory", "")
            way = request.form.get("way", "")
            filter_name = request.form.get("filter", "")
            img = request.files.get("img")
            if not id:
                return '''<script type="text/javascript">
            alert("修改失败: Invalid id!");history.back(-1);</script>'''
            table_id = int(id)
            db = AnimeDataBase(DB_PATH)
            sub_item = ProcessingSubscriptionTable(db)
            mt_item = ProcessingMetaDataTable(db)
            dl_item = ProcessingDownloadTable(db)
            print(request.form.keys())
            if name:
                try:
                    ProcessingNameTable(db).update(table_id, str(name))
                except Exception:
                    return '''<script type="text/javascript">
                            alert("修改失败: Process NameTable Error!");history.back(-1);</script>'''
            if meta:
                try:
                    mt_item.update(table_id, info=str(meta))
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process MetaInfo Error!");history.back(-1);</script>'''
            if img:
                try:
                    new_path = "/static/" + ''.join(sample(string.ascii_letters + string.digits, 16)) + ".jpg"
                    img.save("."+new_path)
                    mt_item.update(table_id, img=new_path)
                except Exception:
                    return '''<script type="text/javascript">
                        alert("修改失败: Process MetaImage Error!");history.back(-1);</script>'''
            if starttime:
                try:
                    startTime = datetime.strptime(str(starttime), HTML_INPUT_TIME_FORMAT)
                    sub_item.update(table_id, starttime=startTime)
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process StartTime Error!");history.back(-1);</script>'''
            if lasttime:
                try:
                    lastTime = datetime.strptime(str(lasttime), HTML_INPUT_TIME_FORMAT)
                    sub_item.update(table_id, lastUpdateTime=lastTime)
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process LastTime Error!");history.back(-1);</script>'''
            if nexttime:
                try:
                    nextTime = datetime.strptime(str(nexttime), HTML_INPUT_TIME_FORMAT)
                    sub_item.update(table_id, nextUpdateTime=nextTime)
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process NextTime Error!");history.back(-1);</script>'''
            if totaleps:
                try:
                    if int(totaleps) > 0:
                        sub_item.update(table_id, totalEpisodes=int(totaleps))
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process TotalEPs Error!");history.back(-1);</script>'''
            if lastep:
                try:
                    if int(lastep) > 0:
                        sub_item.update(table_id, lastUpdateEP=int(lastep))
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process LastEP Error!");history.back(-1);</script>'''
            if nextep:
                try:
                    if int(nextep) > 0:
                        sub_item.update(table_id, nextUpdateEP=int(nextep))
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process NextEP Error!");history.back(-1);</script>'''
            if span:
                try:
                    if int(span) > 0:
                        sub_item.update(table_id, span=int(span))
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process Span Error!");history.back(-1);</script>'''
            if source:
                try:
                    dl_item.update(table_id, source=str(source))
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process Source Error!");history.back(-1);</script>'''
            if directory:
                try:
                    dl_item.update(table_id, directory=str(directory))
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process Directory Error!");history.back(-1);</script>'''
            if way:
                try:
                    dl_item.update(table_id, downloadway=str(way))
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process DownloadWay Error!");history.back(-1);</script>'''
            if filter_name:
                try:
                    dl_item.update(table_id, filter_name=str(filter_name))
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process Filter Error!");history.back(-1);</script>'''
    except Exception as e:
        return f'''<script type="text/javascript">
                                                alert("修改失败: Unexpected Error! {str(e)}");history.back(-1);</script>'''
    finally:
        return redirect(f"detail?id={id}")


if __name__ == '__main__':
    app.run("127.0.0.1", 12138, True)
