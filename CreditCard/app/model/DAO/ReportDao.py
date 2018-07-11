from app import db
from .DBTable import ReportProblem as RP

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

def find_report(u):
    re = db.session.query(RP.id, RP.rep_time, RP.isadvice, RP.pageAdr, RP.content,
        RP.userName, RP.answer, RP.ans_time)\
        .filter(RP.uid == u)\
        .order_by(RP.rep_time)
    return re.all()
