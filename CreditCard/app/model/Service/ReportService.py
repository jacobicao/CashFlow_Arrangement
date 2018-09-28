import app.model.DAO.ReportDao as ReportDao


def report_list(uid,admin=False):
    ll = []
    for v in ReportDao.find_report(uid,admin):
        cl = {}
        cl['id'] = v[0]
        cl['rep_time'] = v[1].strftime("%Y-%m-%d %H:%M:%S")
        cl['isadvice'] = v[2]
        cl['pageAdr'] = v[3]
        cl['content'] = v[4]
        if v[5] is None or v[5] == '':
            cl['userName'] = '匿名'
        else:
            cl['userName'] = v[5]
        cl['answer'] = v[6]
        cl['ans_time'] = v[7].strftime("%Y-%m-%d %H:%M:%S")
        ll.append(cl)
    return {'status':1,'body':{'records':ll}}


def add_one_report(uid, ad, page, content, Name):
    if not str(uid).isdigit():
        return {'msg':'id不存在','status':2}
    if content is '':
        return {'msg':'内容不能为空','status':2}
    try:
        ReportDao.add_reportproblems(uid, ad, page, content, Name)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':2}
    else:
        res = {'msg':'添加成功','status':1}
    return res


def ans_one_answer(id,ans):
    if not str(id).isdigit():
        return {'msg':'id不存在','status':2}
    if ans is '':
        return {'msg':'内容不能为空','status':2}
    try:
        ReportDao.ans_answer(id,ans)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':2}
    else:
        res = {'msg':'添加成功','status':1}
    return res
