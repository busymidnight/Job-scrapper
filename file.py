def save_to_file(file_name, jobs):
  #파일로 읽고 쓰기
  file = open(f"{file_name}.csv", "w") #쓰기전용
  #파일에 헤더 쓰기
  file.write("Position, Company, Location, URL\n")
  
  #파일에 쓰기
  for job in jobs:
    file.write(f"{job['position']},{job['company']},{job['location']},{job['link']}\n")
  
  file.close()