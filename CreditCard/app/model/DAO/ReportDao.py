from app import db
from .DBTable import ReportProblem as RP
import datetime

def add_reportproblems(u, ad, page, content, Name):
    reportproblems = RP(
      uid=u,
      isadvice=ad,
      pageAdr=page,
      content=content,
      userName=Name
      )
    db.session.add(reportproblems)
    db.session.commit()

def find_report(u,admin=False):
    re = db.session.query(RP.id, RP.rep_time, RP.isadvice, RP.pageAdr, RP.content,
        RP.userName, RP.answer, RP.ans_time)
    if not admin:
        re = re.filter(RP.uid == u)
    return re.order_by(RP.rep_time).all()

def ans_answer(rid, ans):
    report = RP.query.get(rid)
    report.ans_time = datetime.datetime.utcnow()
    report.answer = ans
    db.session.add(report)
    db.session.commit()
