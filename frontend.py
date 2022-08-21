# -*- coding:utf-8 -*-
import multiprocessing

import flask
from flask import Flask, request, render_template, redirect

from schedule_work import ScheduleWork
import schedule_work
from multiprocessing import Pool
from GLOBAL_DEFINE import *
from databaseTool import ProcessingNameTable, ProcessingSubscriptionTable, ProcessingMetaDataTable, \
    ProcessingDownloadTable

app = Flask(__name__, static_folder='static')
CONFIG_PATH, DB_PATH, ARIA2_RPC_SERVER, ARIA2_JSONRPC_TOKEN, DEFAULT_CORE_QUANTITY, LOG_DIR, JACKETT_API_LINK_LIST, ERROR_RETRY_SPAN, FILTER_DICTS = app_init()
ss=None

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
                    alert("Error when update:{str(e)}");history.back(-1);</script>'''
    finally:
        ss.reset=True
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
                    alert("Error when update:{str(e)}");history.back(-1);</script>'''
@app.route("/delete",methods=["GET"])
def del_item():
    try:
        if int(request.args.get("id","0"))>0:
            table_id=int(request.args.get("id","0"))
            db = AnimeDataBase(DB_PATH)
            ProcessingMetaDataTable(db).deleteFromMetadataTableByID(table_id)
            ProcessingSubscriptionTable(db).deleteFromDownloadTableByID(table_id)
            ProcessingDownloadTable(db).deleteFromDownloadTableByID(table_id)
            ProcessingNameTable(db).deleteFromNameTableByID(table_id)
            if ProcessingNameTable(db).isInNameTable(table_id=table_id):
                return f'''<script type="text/javascript">
                                    alert("未知原因的删除失败,请重试.");history.back(-1);</script>'''
        db.__del__()
        ss.reset=True
        return redirect(f"all")
    except Exception as e:
        return f'''<script type="text/javascript">
                    alert("Error when update:{str(e)}");history.back(-1);</script>'''



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
            ss.reset=True
    except Exception as e:
        return f'''<script type="text/javascript">
                                                alert("修改失败: Unexpected Error! {str(e)}");history.back(-1);</script>'''
    finally:
        return redirect(f"detail?id={id}")



@app.route("/log")
def watch_log():
    log=""
    name=""
    with open(LOG_DIR+"/"+os.listdir(LOG_DIR)[-1],"r") as fp:
        name+=os.listdir(LOG_DIR)[-1]
        log+=fp.read()
    return f'''
    <!DOCTYPE html >
<html >
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xy-nas-tools</title>
<link href="/static/css.css" rel="stylesheet" type="text/css" />
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
  <table width=80% height="85%" border="0" align="center" class="main">
  <tr><th height="20px" align="center">{name}</th></tr>
    <tr>
      <td align="center"><textarea class="log1" readonly="readonly">{log}</textarea>

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


@app.route("/setting",methods=["GET","POST"])
def setting():
    if request.method=="POST":
        try:
            global DB_PATH, ARIA2_RPC_SERVER, ARIA2_JSONRPC_TOKEN, DEFAULT_CORE_QUANTITY, LOG_DIR, JACKETT_API_LINK_LIST, ERROR_RETRY_SPAN, FILTER_DICTS
            DB_PATH = request.form.get("DB_PATH", DB_PATH)
            ARIA2_RPC_SERVER = request.form.get("ARIA2_RPC_SERVER", ARIA2_RPC_SERVER)
            ARIA2_JSONRPC_TOKEN = request.form.get("ARIA2_JSONRPC_TOKEN", ARIA2_JSONRPC_TOKEN)
            DEFAULT_CORE_QUANTITY = request.form.get("DEFAULT_CORE_QUANTITY", DEFAULT_CORE_QUANTITY)
            LOG_DIR = request.form.get("LOG_DIR", LOG_DIR)
            if request.form.get("JACKETT_API_LINK_LIST", ""):
                tmp = request.form.get("JACKETT_API_LINK_LIST", "").split("\n")
                result_tmp=[]
                for i in tmp:
                    i=i.replace("\n", "").replace("\r","").replace("\r","").replace("\r","")
                    if i:
                        result_tmp.append(i)
                JACKETT_API_LINK_LIST = result_tmp
            DB_PATH = request.form.get("DB_PATH", DB_PATH)
            if request.form.get("filter_name",""):
                if request.form.get("filter_name","") not in FILTER_DICTS.keys():
                    FILTER_DICTS[request.form.get("filter_name","")]={"episode": "0", "reject_rules": [], "including_rules": []}
            if request.form.get("filter_exclude", ""):
                tmp = request.form.get("filter_exclude", "").split(";")
                for i in tmp:
                    i.replace(";", "")
                    if not i:
                        tmp.remove("")
                if request.form.get("filter_name", ""):
                    FILTER_DICTS[str(request.form.get("filter_name", ""))]["reject_rules"] = tmp
            if request.form.get("filter_include", ""):
                tmp = request.form.get("filter_include", "").split(";")
                for i in tmp:
                    i.replace(";", "")
                    if not i:
                        tmp.remove("")
                if request.form.get("filter_name", ""):
                    FILTER_DICTS[str(request.form.get("filter_name", ""))]["including_rules"] = tmp
            with open(CONFIG_PATH,"w") as fp:



                paras_json = {
                    'CONFIG_PATH': CONFIG_PATH,
                    'DB_PATH': DB_PATH,
                    'ARIA2_RPC_SERVER': ARIA2_RPC_SERVER,
                    'ARIA2_JSONRPC_TOKEN': ARIA2_JSONRPC_TOKEN,
                    'DEFAULT_CORE_QUANTITY': DEFAULT_CORE_QUANTITY,
                    'LOG_DIR': LOG_DIR,
                    'JACKETT_API_LINK_LIST': JACKETT_API_LINK_LIST,
                    'ERROR_RETRY_SPAN': ERROR_RETRY_SPAN,
                    'FILTER_DICTS': FILTER_DICTS,
                }
                json.dump(paras_json, fp)
            app_init()
            return f'''<script type="text/javascript">
                       alert("设置成功!");history.back(-1);</script>'''
        except Exception as e:
            return f'''<script type="text/javascript">
                        alert("修改失败: Unexpected Error! {str(e)}");history.back(-1);</script>'''
    else:
        html= f'''
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
       <form action="/setting" method="post">
      <table width=80%  border="1" align="center" cellpadding="1" cellspacing="0" class="main">
        <tr height="60px">
        <td width="50%" align="center">CONFIG_PATH</td>
        <td width="50%" align="center"><input type="text" value="{CONFIG_PATH}" class="text1" name="source" readonly="readonly"></td>
      </tr>
        <tr height="60px">
        <td width="50%" align="center">DB_PATH</td>
        <td width="50%" align="center"><input type="text" value="{DB_PATH}" class="text1" name="DB_PATH"></td>
      </tr>
        <tr height="60px">
        <td width="50%" align="center">ARIA2_JSONRPC_TOKEN</td>
        <td width="50%" align="center"><input type="text" value="{ARIA2_JSONRPC_TOKEN}" class="text1" name="ARIA2_JSONRPC_TOKEN"></td>
      </tr>
        <tr height="60px">
        <td width="50%" align="center">DEFAULT_CORE_QUANTITY</td>
        <td width="50%" align="center"><input type="number" value="{DEFAULT_CORE_QUANTITY}" class="text1" name="DEFAULT_CORE_QUANTITY"></td>
      </tr>
        <tr height="60px">
        <td width="50%" align="center">LOG_DIR</td>
        <td width="50%" align="center"><input type="text" value="{LOG_DIR}" class="text1" name="LOG_DIR"></td>
      </tr>
        <tr height="150px">
        <td width="50%" align="center">JACKETT_API_LINK_LIST</td><td width="50%" align="center"><textarea class="textarea1" name="JACKETT_API_LINK_LIST">'''
    for i in JACKETT_API_LINK_LIST:
        html+=i+"&#10&#10"
    html+=f'''</textarea></td></tr>
        <tr height="60px">
        <td width="50%" align="center">ERROR_RETRY_SPAN</td>
        <td width="50%" align="center"><input type="number" value="{ERROR_RETRY_SPAN}" class="text1" name="ERROR_RETRY_SPAN">h</td>
      </tr>
      </table>
         <table width=80%  border="1" align="center" cellpadding="1" cellspacing="0" class="main">
        <tr height="60px">
        <td colspan="2" align="center">过滤条件</td></tr>
        <tr height="60px"><td width="50%" align="center">选择</td>
        <td width="50%" align="center">
          <select class="text1" onchange="filter_select_changed();" id="filter_name">'''
    for i in FILTER_DICTS.keys():
        html+=f"<option>{i}</option>"
    html+='''
            <option>新建...</option>
          </select>
          <script>'''
    html+="var filter_name_list={};"
    for i in FILTER_DICTS.keys():
        html+=f'''filter_name_list["{i}"]={json.dumps(FILTER_DICTS.get(i),ensure_ascii=False)};'''
    html+='''
            function filter_select_changed(){
                var source = document.getElementById("filter_name");
                var name = document.getElementById("filter_name_edited");
                var exclude = document.getElementById("filter_exclude");
                var include = document.getElementById("filter_include");
                var display_name = source.options[source.selectedIndex].value
                if (display_name=="新建..."){
                name.setAttribute("value","");
                exclude.setAttribute("value","");
                include.setAttribute("value","");}
                else{
                name.setAttribute("value",display_name);
                var exclude_result=new String(filter_name_list[source.options[source.selectedIndex].value]["reject_rules"])
                var include_result=new String(filter_name_list[source.options[source.selectedIndex].value]["including_rules"])
                exclude.setAttribute("value",exclude_result.replaceAll(",",";"));
                include.setAttribute("value",include_result.replaceAll(",",";"));}
    
    
            }
          </script>
        </td>
      </tr>
           <tr height="60px">
        <td width="50%" align="center">规则名称</td>
        <td width="50%" align="center"><input type="text" value="default" class="text1" name="filter_name" id="filter_name_edited"></td>
      </tr>
        <tr height="60px">
        <td width="50%" align="center">排除规则(正则,用;分隔)</td>
        <td width="50%" align="center"><input type="text" value="" class="text1" name="filter_exclude" id="filter_exclude"></td>
      </tr>
           <tr height="60px">
        <td width="50%" align="center">包含规则(正则,用;分隔)</td>
        <td width="50%" align="center"><input type="text" value="" class="text1" name="filter_include" id="filter_include"></td>
      </tr>
      </table>
    
      <table width="100%" height="80" border="0" cellpadding="0" cellspacing="0" class="buttons">
      <tr>
        <td  align="right">
          <button class="button2" onclick="javascript :history.back(-1);">返回</button>
          <button class="button1" type="submit">提交</button>
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


@app.route("/about")
def about():
    return '''<!DOCTYPE html >
<html >
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xy-nas-tools</title>
<link href="/static/css.css" rel="stylesheet" type="text/css" />
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
<table width=80% border="1" height="85%" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr height=300px><td><textarea class="about" readonly="readonly" text-align="center">&#10&#10Thanks for using xy-nas-tool!&#10 xy-nas-tool  made by xy.&#10Github  @xyseer&#10Docker  @xyseer &#10 If you have problem while using this, please let me know on the Github Project.&#10 Enjoy & have fun!</textarea></td></tr>
  <tr height="80%"><td width="80%"><video width="100%" align="center" src="/static/about.mp4" autoplay="autoplay" controls="controls"></video></td></tr>

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



def main():
    try:
        global ss
        CONFIG_PATH, DB_PATH, ARIA2_JSONRPC_TOKEN, ARIA2_RPC_SERVER, DEFAULT_CORE_QUANTITY, LOG_DIR, JACKETT_API_LINK_LIST, ERROR_RETRY_SPAN,FILTER_DICTS=app_init()
        ss = ScheduleWork(DEFAULT_CORE_QUANTITY)
        sw = multiprocessing.Process(target=ss.main_schedule)
        sw.start()
        print("ababab")
        app.run("0.0.0.0", 12138)
        journal_write("================MAIN PROCESS UNEXPECTED EXIT=================")
    except KeyboardInterrupt:
        journal_write("================MAIN PROCESS TERMINATE=================")
        pass
    except InterruptedError:
        journal_write("================MAIN PROCESS TERMINATE=================")
        pass
    except Exception as e:
        print(e)
        exit(-1)
