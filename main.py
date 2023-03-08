from flask import Flask, render_template, request, redirect, send_file
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

app = Flask(__name__)

#가짜 데이터베이스 만들기, 이미 검색된 걸 또 불러오지 않도록(속도향상)
#서버가 켜있을때만 유지되는 데이터베이스
db = {}

@app.route("/") #데코레이터가 함수를 데코레이팅 할 때만 함수를 실행
def home():
  return render_template("home.html")

@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword in db:
    jobs = db[keyword]
  else:
    indeed = extract_indeed_jobs(keyword)
    wwr = extract_wwr_jobs(keyword)
    jobs = indeed + wwr
    db[keyword] = jobs
  return render_template("search.html", keyword=keyword, jobs = jobs)

@app.route("/export")
def export():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword not in db:
    return redirect(f"/search?keyword={keyword}")
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}.csv",as_attachment=True)

if __name__ == '__main__':
    app.run("127.0.0.1")