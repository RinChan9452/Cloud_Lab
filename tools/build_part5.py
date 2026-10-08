"""Part 5 content (Thai). Usage: python build_part5.py <unpacked_docx_dir> "D:/Cloud lab/Part 5" """
import sys
from report_lib import H, SUB, P, STEP, BUL, BOX, CODE, TABLE, PAGEBREAK, Images, load_photos, splice_part

UN, PHOTOS = sys.argv[1], sys.argv[2]
photos = load_photos(PHOTOS)
def photo(key, idx=0):
    return photos[key][idx]
IMG = Images(UN, 'part5', docpr_base=5000)

X = []
add = X.append

LB_DNS = 'myLB-334706066.us-east-1.elb.amazonaws.com'

# ---------- Intro ----------
add(P('Part 5 เป็นการเรียนรู้การปรับขนาดแนวนอน (Horizontal scaling) คือการเพิ่มหรือลด**จำนวนเครื่อง**ตามปริมาณงาน '
      'แทนการเปลี่ยนเครื่องให้ใหญ่ขึ้น (Vertical scaling) โดยใช้ **Amazon EC2 Auto Scaling** ร่วมกับ Elastic Load Balancer'))
add(BUL('**Auto Scaling** – สร้าง Launch template และ Auto Scaling group แล้วทดสอบว่าเมื่อเครื่องถูกลบ ระบบจะสร้างเครื่องใหม่แทนให้อัตโนมัติ'))
add(BUL('**ELB & Auto scaling** – ทำ Web server ด้วย Docker และ Nginx บน Ubuntu สร้าง AMI แล้วให้ Auto Scaling group '
        'สร้างเครื่องหลัง Load Balancer และเพิ่ม/ลดจำนวนเครื่องตามการใช้ CPU'))
add(BUL('**CloudWatch** – ดูค่า metric ของเครื่อง EC2 ตั้ง Alarm ให้ส่งอีเมลเมื่อ CPU สูงเกินกำหนด และสร้าง Dashboard'))
add(BOX('**ก่อนเริ่ม:** ทุกขั้นตอนทำใน Region **United States (N. Virginia) us-east-1** และใช้ Key pair **MyKPuseast2** '
        'กับ Security Group **MySGuseast2** จาก Part 1 ถ้ายังมี Load Balancer myLB, Target group myTG หรือ Launch template ชื่อ myLT '
        'จาก Part ก่อน ให้ลบก่อน เพราะแลปนี้ใช้ชื่อเดิม'))
add(TABLE(['คำศัพท์', 'ความหมาย'],
          [['Launch template', 'แม่แบบการสร้างเครื่อง เก็บ AMI, Instance type, Key pair, Security group ไว้ให้ Auto Scaling ใช้'],
           ['Auto Scaling group (ASG)', 'กลุ่มเครื่องที่ AWS ดูแลจำนวนให้อัตโนมัติตามค่า Desired / Min / Max'],
           ['Desired capacity', 'จำนวนเครื่องที่ต้องการให้มีตอนนี้'],
           ['Min / Max desired capacity', 'จำนวนเครื่องน้อยที่สุด / มากที่สุดที่ ASG ปรับได้'],
           ['Scale out / Scale in', 'เพิ่มเครื่อง / ลดเครื่อง'],
           ['Target tracking scaling policy', 'กฎที่ให้ ASG ปรับจำนวนเครื่องเพื่อรักษาค่า metric (เช่น CPU เฉลี่ย) ให้ใกล้เป้าหมาย']],
          [2800, 6200]))

# =====================================================================
# 13. Auto Scaling
# =====================================================================
add(H('13. Auto Scaling'))
add(SUB('วัตถุประสงค์'))
add(P('**Amazon EC2 Auto Scaling** ดูแลให้มีจำนวนเครื่อง EC2 ตามที่กำหนดอยู่เสมอ ถ้าเครื่องใดเสียหรือถูกลบ ASG จะตรวจพบผ่าน '
      'Health check แล้วสร้างเครื่องใหม่แทนให้อัตโนมัติ (Self-healing) และยังเพิ่ม/ลดจำนวนเครื่องตามปริมาณงานได้ (หัวข้อที่ 14)'))
add(P('ในหัวข้อนี้จะสร้าง Launch template ที่ใช้ Amazon Linux แล้วสร้าง Auto Scaling group ขนาด 1 เครื่อง '
      'จากนั้นทดลองลบเครื่องทิ้งเพื่อดูว่า ASG สร้างเครื่องใหม่แทนหรือไม่'))
add(SUB('ส่วน A: สร้าง Launch template'))
add(STEP('13.1', 'ไปที่ EC2 → เมนู **Instances** → **Launch Templates** แล้วคลิก **Create launch template**'))
add(IMG(photo('1'), 'รูปที่ 13.1 หน้า Launch Templates'))
add(STEP('13.2', 'ตั้งค่าส่วนบน'))
add(BUL('Launch template name: **myLT**'))
add(BUL('Application and OS Images: แท็บ **Quick Start** → **Amazon Linux** → **Amazon Linux 2023 kernel-6.18 AMI** (Free tier eligible)'))
add(IMG(photo('2'), 'รูปที่ 13.2 ตั้งชื่อ myLT และเลือก Amazon Linux 2023'))
add(STEP('13.3', 'ตั้งค่าส่วนล่าง แล้วคลิก **Create launch template**'))
add(BUL('Instance type: เปิด All generations → **m7i-flex.large**'))
add(BUL('Key pair: **Don\'t include in launch template** (แลปนี้ไม่ต้องล็อกอินเข้าเครื่อง)'))
add(BUL('Subnet และ Availability Zone: **Don\'t include in launch template** (ให้ ASG เป็นผู้เลือก)'))
add(BUL('Firewall: **Select existing security group** → **MySGuseast2**'))
add(BUL('Storage: ใช้ค่าเริ่มต้น **8 GiB gp3**'))
add(IMG(photo('3'), 'รูปที่ 13.3 ตั้งค่า Instance type, Network และ Storage'))
add(BOX('**Subnet ใน Launch template:** ต้องปล่อยเป็น Don\'t include เพราะ Auto Scaling group จะกระจายเครื่องไปหลาย Subnet/AZ เอง '
        'ถ้าระบุ Subnet ไว้ในแม่แบบ เครื่องทุกเครื่องจะถูกสร้างใน Subnet เดียว'))
add(STEP('13.4', 'หน้า Launch templates จะมี **myLT** (lt-0e04c8a87597c1ac4) Default version 1'))
add(IMG(photo('4'), 'รูปที่ 13.4 Launch template myLT'))
add(SUB('ส่วน B: สร้าง Auto Scaling group'))
add(STEP('13.5', 'ไปที่เมนู **Auto Scaling** → **Auto Scaling Groups** แล้วคลิก **Create Auto Scaling group** '
                 '(แผนภาพ How it works แสดงความสัมพันธ์ของ Minimum size, Desired capacity และ Maximum size)'))
add(IMG(photo('5'), 'รูปที่ 13.5 หน้า Amazon EC2 Auto Scaling'))
add(STEP('13.6', 'Step 1: ตั้ง Auto Scaling group name = **myASG** เลือก Launch template = **myLT** Version **Default (1)** แล้วคลิก **Next**'))
add(IMG(photo('6'), 'รูปที่ 13.6 ตั้งชื่อ myASG และเลือก myLT'))
add(STEP('13.7', 'Step 2: เลือก VPC = **Default VPC** และ Availability Zones and subnets = **use1-az1 (us-east-1a)** '
                 '(เลือก AZ ใดก็ได้) Availability Zone distribution = **Balanced best effort**'))
add(IMG(photo('7'), 'รูปที่ 13.7 เลือก VPC และ Subnet'))
add(STEP('13.8', 'คลิก **Skip to review** (ข้าม Step 3–6 เพราะยังไม่ต้องใช้ Load Balancer และ Scaling policy) แล้วคลิก '
                 '**Create Auto Scaling group** ค่าเริ่มต้นคือ Desired 1, Min 1, Max 1 ASG จะมีสถานะ **Updating capacity** ระหว่างสร้างเครื่อง'))
add(IMG(photo('8'), 'รูปที่ 13.8 myASG ที่สร้างเสร็จ'))
add(STEP('13.9', 'คลิก myASG → แท็บ **Instance management** จะเห็นเครื่องที่ ASG สร้าง (i-0f98e3f76748866ab) '
                 'Lifecycle **InService** และ Health status **Healthy**'))
add(IMG(photo('9'), 'รูปที่ 13.9 เครื่องที่ ASG สร้างให้'))
add(STEP('13.10', 'แท็บ **Activity** → **Activity history** จะบันทึกทุกการกระทำของ ASG พร้อมสาเหตุ เช่น '
                  '**Launching a new EC2 instance** เพราะ Desired capacity เปลี่ยนจาก 0 เป็น 1 ใช้หน้านี้ตรวจสอบว่า ASG ทำงานถูกต้อง'))
add(IMG(photo('10'), 'รูปที่ 13.10 Activity history ของ myASG'))
add(SUB('ส่วน C: ทดสอบ Self-healing'))
add(STEP('13.11', 'ไปที่ **Instances** ติ๊กเลือกเครื่องของ ASG (สังเกตว่า Auto Scaling Group name = myASG) → **Instance state** → '
                  '**Terminate (delete) instance** เครื่องจะเปลี่ยนเป็น **Shutting-down**'))
add(IMG(photo('11', 1), 'รูปที่ 13.11 ลบเครื่องที่ ASG สร้าง'))
add(STEP('13.12', 'กลับไปที่ myASG → แท็บ Activity จะเห็น 2 รายการใหม่'))
add(BUL('**Terminating EC2 instance** – เครื่องถูกนำออกเพราะ EC2 health check พบว่าถูก terminate'))
add(BUL('**Launching a new EC2 instance** (i-0acff7191364836d8) – สร้างเครื่องใหม่แทนเครื่องที่ unhealthy'))
add(IMG(photo('11', 0), 'รูปที่ 13.12 ASG สร้างเครื่องใหม่แทนอัตโนมัติ'))
add(STEP('13.13', 'หน้า Instances จะมีเครื่องใหม่ (Running, Public IP 98.86.182.102) และเครื่องเดิมเป็น Terminated '
                  'แสดงว่า ASG รักษาจำนวนเครื่องให้เท่ากับ Desired capacity ได้จริง'))
add(IMG(photo('12'), 'รูปที่ 13.13 เครื่องใหม่จาก Auto Scaling'))
add(STEP('13.14', 'เมื่อทดสอบเสร็จ ให้ลบ **myASG** (Auto Scaling Groups → Actions → **Delete**) เครื่องในกลุ่มจะถูกลบตามไปด้วย '
                  'และลบ Launch template **myLT** เพราะหัวข้อที่ 14 จะสร้างชื่อเดิมใหม่', keep_next=False))
add(BOX('**ห้ามลบเครื่องของ ASG ด้วยการ Terminate อย่างเดียว:** ASG จะสร้างเครื่องใหม่ขึ้นมาแทนทันที '
        'ถ้าต้องการลบเครื่องทั้งหมดต้องลบ ASG หรือตั้ง Desired / Min เป็น 0'))

# =====================================================================
# 14. ELB & Auto scaling
# =====================================================================
add(H('14. ELB & Auto scaling'))
add(SUB('วัตถุประสงค์'))
add(P('รวม Load Balancer (Part 4) กับ Auto Scaling เข้าด้วยกัน: ผู้ใช้เข้าเว็บผ่าน DNS name ของ Load Balancer ชื่อเดียว '
      'ส่วน Auto Scaling group จะสร้างเครื่องจาก AMI และ**ลงทะเบียนเข้า Target group ให้อัตโนมัติ** เมื่อ CPU สูงเกินเป้าหมายจะเพิ่มเครื่อง (Scale out) '
      'และเมื่อลดความต้องการจะลดเครื่อง (Scale in)'))
add(P('Web server ในหัวข้อนี้ใช้ **Ubuntu + Docker + Nginx** ซึ่งเบากว่า Windows + XAMPP มาก และตั้งค่าให้ container เริ่มเองเมื่อเปิดเครื่อง '
      'ทำให้เครื่องที่ ASG สร้างจาก AMI พร้อมให้บริการทันทีโดยไม่ต้องเข้าไปตั้งค่า'))
add(TABLE(['ทรัพยากร', 'ชื่อ', 'ค่าที่ใช้'],
          [['เครื่องต้นแบบ', 'i-028ffde8c374c7aa1', 'Ubuntu 26.04, m7i-flex.large, Docker + Nginx (ลบหลังสร้าง AMI)'],
           ['AMI', 'myAMI', 'สร้างจากเครื่องต้นแบบ'],
           ['Load balancer', 'myLB', 'Application, Internet-facing, us-east-1a + us-east-1b'],
           ['Target group', 'myTG', 'Instances, HTTP:80, เริ่มต้นไม่มี target'],
           ['Launch template', 'myLT', 'myAMI, m7i-flex.large, MyKPuseast2, MySGuseast2'],
           ['Auto Scaling group', 'myASG', 'Desired 1, Min 1, Max 2, ผูกกับ myTG']],
          [2200, 2400, 4400]))

add(SUB('ส่วน A: สร้างเครื่องต้นแบบ Ubuntu'))
add(STEP('14.1', 'สร้าง EC2 ใหม่ด้วย AMI **Ubuntu** (Quick Start → Ubuntu), Instance type **m7i-flex.large**, Key pair **MyKPuseast2**, '
                 'Default VPC, Auto-assign public IP **Enable**, Security group **MySGuseast2** (ภาพหน้าตั้งค่าไม่ได้บันทึกไว้ ใช้วิธีเดียวกับ Part 1 หัวข้อที่ 3) '
                 'ในแลปนี้ได้เครื่อง i-028ffde8c374c7aa1 ที่ us-east-1c, Public IP 100.55.56.144 '
                 '(รูปนี้ยังเห็นเครื่องจากหัวข้อที่ 13 เป็น Terminated)'))
add(IMG(photo('13'), 'รูปที่ 14.1 เครื่องต้นแบบ Ubuntu'))
add(STEP('14.2', 'แก้ Inbound rules ของ **MySGuseast2** (Security Groups → MySGuseast2 → Edit inbound rules) คลิก **Add rule** '
                 'เพิ่ม Type **SSH** (TCP 22) Source **Anywhere-IPv4 (0.0.0.0/0)** แล้วคลิก **Save rules** '
                 'เพราะเครื่อง Linux เชื่อมต่อด้วย SSH ไม่ใช่ RDP'))
add(IMG(photo('14'), 'รูปที่ 14.2 เพิ่ม Inbound rule SSH'))
add(STEP('14.3', 'ติ๊กเลือกเครื่อง → **Connect** → แท็บ **EC2 Instance Connect** (Public subnet access) ตั้ง **Username = ubuntu** '
                 '(ค่าเริ่มต้นเป็น ec2-user ซึ่งใช้กับ Amazon Linux เท่านั้น) แล้วคลิก **Connect**'))
add(IMG(photo('15'), 'รูปที่ 14.3 Connect ด้วย EC2 Instance Connect'))
add(STEP('14.4', 'จะเปิด Terminal บนเบราว์เซอร์ แสดง **Welcome to Ubuntu 26.04 LTS** และ prompt '
                 '**ubuntu@ip-172-31-30-165:~$** พร้อมพิมพ์คำสั่ง'))
add(IMG(photo('16'), 'รูปที่ 14.4 Terminal ของ Ubuntu'))
add(BOX('**การวางคำสั่งใน Terminal บนเบราว์เซอร์:** กด **Ctrl + Shift + V** (หรือคลิกขวา → Paste) Ctrl + V อย่างเดียวอาจใช้ไม่ได้'))

add(SUB('ส่วน B: ติดตั้ง Docker'))
add(STEP('14.5', 'พิมพ์คำสั่งต่อไปนี้**ทีละบรรทัด** รอให้แต่ละคำสั่งทำงานเสร็จก่อนพิมพ์คำสั่งถัดไป'))
add(CODE(['sudo apt update',
          'sudo apt install -y apt-transport-https ca-certificates curl software-properties-common',
          'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg',
          'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] '
          'https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" '
          '| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null',
          'sudo apt update',
          'sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin',
          'sudo docker run hello-world']))
add(TABLE(['คำสั่ง', 'ทำอะไร'],
          [['apt update / apt install ... curl ...', 'อัปเดตรายการแพ็กเกจ และติดตั้งเครื่องมือที่ใช้ดาวน์โหลดแบบ HTTPS'],
           ['curl ... | gpg --dearmor', 'ดาวน์โหลดกุญแจ GPG ของ Docker เพื่อยืนยันว่าแพ็กเกจมาจาก Docker จริง'],
           ['echo "deb ..." | tee docker.list', 'เพิ่มแหล่งดาวน์โหลด (repository) ของ Docker สำหรับ Ubuntu เวอร์ชันนี้'],
           ['apt install docker-ce ...', 'ติดตั้ง Docker Engine, CLI, containerd และ plugin'],
           ['docker run hello-world', 'ทดสอบ Docker ด้วย container ตัวอย่าง']],
          [3600, 5400]))
add(IMG(photo('17'), 'รูปที่ 14.5 คำสั่งติดตั้ง Docker'))
add(STEP('14.6', 'หลังคำสั่งสุดท้าย ถ้าเห็นข้อความ **Hello from Docker! This message shows that your installation appears to be working correctly.** '
                 'แสดงว่าติดตั้ง Docker สำเร็จ (Docker ดาวน์โหลด image hello-world จาก Docker Hub มารันให้)'))
add(IMG(photo('18'), 'รูปที่ 14.6 Hello from Docker!'))

add(SUB('ส่วน C: รัน Nginx ใน Docker container'))
add(STEP('14.7', 'สร้างโฟลเดอร์สำหรับหน้าเว็บ แล้วสร้างไฟล์ index.html ด้วย nano'))
add(CODE(['mkdir -p ~/nginx-site/html',
          'nano ~/nginx-site/html/index.html']))
add(P('ใน nano ให้วางโค้ด HTML นี้ (เปลี่ยน <your name> เป็นชื่อของเรา) แล้วกด **Ctrl + O** → **Enter** เพื่อบันทึก และ **Ctrl + X** เพื่อออก '
      '(หรือกด Ctrl + X → Y → Enter)'))
add(CODE('<html><head>hello page</head><body>Hello <your name></body></html>'))
add(STEP('14.8', 'รัน Nginx เป็น container'))
add(CODE('sudo docker run --name my-nginx -p 80:80 -d --restart=unless-stopped '
         '-v /home/ubuntu/nginx-site/html:/usr/share/nginx/html nginx'))
add(TABLE(['ส่วนของคำสั่ง', 'ความหมาย'],
          [['--name my-nginx', 'ตั้งชื่อ container'],
           ['-p 80:80', 'เปิดพอร์ต 80 ของเครื่องให้ส่งต่อไปยังพอร์ต 80 ใน container'],
           ['-d', 'รันเบื้องหลัง (detached)'],
           ['--restart=unless-stopped', 'ให้ container เริ่มทำงานเองทุกครั้งที่เครื่อง Ubuntu เปิดใหม่ (สำคัญมากสำหรับเครื่องที่สร้างจาก AMI)'],
           ['-v /home/ubuntu/nginx-site/html:/usr/share/nginx/html', 'นำโฟลเดอร์หน้าเว็บของเราไปแทนโฟลเดอร์หน้าเว็บของ Nginx'],
           ['nginx', 'ชื่อ image ที่ Docker ดาวน์โหลดจาก Docker Hub']],
          [4000, 5000]))
add(IMG(photo('19'), 'รูปที่ 14.7 คำสั่ง Deploy Nginx container'))
add(STEP('14.9', 'Docker จะดาวน์โหลด image **nginx:latest** (Unable to find image locally → Pulling from library/nginx → '
                 'Downloaded newer image) แล้วแสดง Container ID ยาวๆ แปลว่า container เริ่มทำงานแล้ว'))
add(IMG(photo('20'), 'รูปที่ 14.8 Nginx container เริ่มทำงาน'))
add(BOX('**ลำดับคำสั่ง:** ในรูปที่ 14.8 คำสั่ง nano ถูกพิมพ์ก่อน mkdir ครั้งหนึ่ง ซึ่งจะบันทึกไฟล์ไม่ได้เพราะยังไม่มีโฟลเดอร์ '
        'ให้รัน **mkdir ก่อนเสมอ** แล้วจึงสร้างไฟล์ด้วย nano'))
add(STEP('14.10', 'จากคอมพิวเตอร์ของเรา เปิด **http://100.55.56.144** (Public IP ของเครื่องต้นแบบ) จะเห็น **hello pageHello Sono-G** '
                  '(ข้อความใน <head> และ <body> แสดงติดกันเพราะไม่ได้ใช้แท็ก <title>)'))
add(IMG(photo('21'), 'รูปที่ 14.9 เปิดหน้าเว็บ Nginx จากคอมพิวเตอร์ของเรา'))

add(SUB('ส่วน D: สร้าง AMI จากเครื่องต้นแบบ'))
add(STEP('14.11', 'ที่ Instances ติ๊กเลือกเครื่องต้นแบบ → **Actions** → **Image and templates** → **Create image**'))
add(IMG(photo('22'), 'รูปที่ 14.10 Create image จากเครื่องต้นแบบ'))
add(STEP('14.12', 'ตั้ง Image name = **myAMI** ไม่ต้องติ๊ก Reboot instance ใช้ volume เดิม (8 GiB gp3) แล้วคลิก **Create image**'))
add(IMG(photo('23'), 'รูปที่ 14.11 ตั้งค่า Create image'))
add(STEP('14.13', 'รอจน myAMI มีสถานะ **Available** (Images → AMIs) แล้วจึง **Terminate** เครื่องต้นแบบได้ '
                  'เพราะต่อจากนี้ ASG จะสร้างเครื่องจาก myAMI เอง'))
add(IMG(photo('24'), 'รูปที่ 14.12 Terminate เครื่องต้นแบบหลัง AMI พร้อม'))
add(BOX('**อย่า Terminate ก่อน AMI เป็น Available:** ถ้าลบเครื่องขณะ AMI ยัง Pending อาจทำให้สร้าง AMI ไม่สำเร็จ'))

add(SUB('ส่วน E: สร้าง Load Balancer และ Target group'))
add(STEP('14.14', 'ไปที่ **Load Balancers** → **Create load balancer** → เลือก **Application Load Balancer** → **Create**'))
add(IMG(photo('25'), 'รูปที่ 14.13 เลือก Application Load Balancer'))
add(STEP('14.15', 'ตั้งค่า Basic configuration และ Network mapping'))
add(BUL('Load balancer name: **myLB**, Scheme: **Internet-facing**, IP address type: **IPv4**'))
add(BUL('VPC: **Default VPC**'))
add(BUL('Availability Zones and subnets: ติ๊ก **us-east-1a** (subnet-0a1e0ab754b787615) และ **us-east-1b** (subnet-09981e1d033de9c5c) '
        '(จดไว้ เพราะ ASG ต้องใช้ AZ เดียวกัน)'))
add(IMG(photo('26'), 'รูปที่ 14.14 ตั้งค่า myLB และเลือก 2 AZ'))
add(STEP('14.16', 'Security groups: **MySGuseast2** ที่ Listener **HTTP:80** เลือก **Forward to target groups** '
                  'แล้วคลิกลิงก์ **create target group** (เปิดแท็บใหม่)'))
add(IMG(photo('27'), 'รูปที่ 14.15 คลิก create target group'))
add(STEP('14.17', 'ตั้งค่า Target group: Target type **Instances**, name **myTG**, Protocol **HTTP**, Port **80**, IP address type **IPv4**, '
                  'VPC **Default**, Protocol version **HTTP1**'))
add(IMG(photo('29'), 'รูปที่ 14.16 ตั้งค่า Target group myTG'))
add(STEP('14.18', 'เลื่อนลงไปที่ **Health checks** (Protocol HTTP, Path /) เปิด **Advanced health check settings** แล้วตั้งค่าเหมือน Part 4 '
                  'ขั้นตอนที่ 12.23 ตั้งแต่ตอนสร้าง: Healthy threshold **2**, Unhealthy threshold **2**, Timeout **14** วินาที, '
                  'Interval **15** วินาที, Success codes **200-499** แล้วคลิก **Next**'))
add(IMG(photo('28'), 'รูปที่ 14.17 ตั้งค่า Health checks'))
add(STEP('14.19', 'หน้า **Register targets** ไม่ต้องเลือกเครื่องใด (Available instances = 0 เพราะลบเครื่องต้นแบบแล้ว) '
                  'คลิก **Next** แล้ว **Create target group** เครื่องจะถูกเพิ่มเข้า myTG โดย Auto Scaling group ภายหลัง'))
add(IMG(photo('30'), 'รูปที่ 14.18 ไม่ต้องลงทะเบียน target เอง'))
add(STEP('14.20', 'กลับไปที่แท็บสร้าง Load Balancer กดปุ่ม Refresh ข้างช่อง Target group แล้วเลือก **myTG** '
                  'จากนั้นเลื่อนลงไปคลิก **Create load balancer**'))
add(IMG(photo('31'), 'รูปที่ 14.19 เลือก myTG แล้วสร้าง Load Balancer'))

add(SUB('ส่วน F: สร้าง Launch template จาก AMI'))
add(STEP('14.21', 'ไปที่ **Launch Templates** → **Create launch template** ตั้ง name = **myLT** และที่ AMI เลือกแท็บ **My AMIs** → '
                  '**Owned by me** → **myAMI**'))
add(IMG(photo('32'), 'รูปที่ 14.20 Launch template ที่ใช้ myAMI'))
add(STEP('14.22', 'ตั้งค่าส่วนล่าง แล้วคลิก **Create launch template**'))
add(BUL('Instance type: เปิด All generations → **m7i-flex.large**'))
add(BUL('Key pair: **MyKPuseast2** (ใส่ไว้เพื่อให้ SSH เข้าเครื่องที่ ASG สร้างได้ถ้าต้องแก้ปัญหา)'))
add(BUL('Subnet และ Availability Zone: **Don\'t include in launch template**'))
add(BUL('Firewall: **Select existing security group** → **MySGuseast2**'))
add(BUL('Storage: ใช้ค่าจาก AMI (8 GiB gp3)'))
add(IMG(photo('33'), 'รูปที่ 14.21 ตั้งค่า Instance type, Key pair และ Security group'))

add(SUB('ส่วน G: สร้าง Auto Scaling group ที่ผูกกับ Load Balancer'))
add(STEP('14.23', 'ไปที่ **Auto Scaling Groups** → **Create Auto Scaling group** ตั้ง name = **myASG** เลือก Launch template **myLT** '
                  'Version **Default (1)** แล้วคลิก **Next**'))
add(IMG(photo('34'), 'รูปที่ 14.22 ตั้งชื่อ myASG และเลือก myLT'))
add(STEP('14.24', 'VPC = **Default VPC** และ Availability Zones and subnets เลือก**ให้ตรงกับ Load Balancer**: '
                  '**us-east-1a** (subnet-0a1e0ab754b787615) และ **us-east-1b** (subnet-09981e1d033de9c5c) แล้วคลิก **Next**'))
add(IMG(photo('35'), 'รูปที่ 14.23 เลือก AZ เดียวกับ myLB'))
add(STEP('14.25', 'Step 3 Integrate with other services: Load balancing เลือก **Attach to an existing load balancer** → '
                  '**Choose from your load balancer target groups** → **myTG | HTTP** (Application Load Balancer: myLB) '
                  'VPC Lattice เลือก **No VPC Lattice service**'))
add(IMG(photo('36'), 'รูปที่ 14.24 ผูก ASG กับ Target group myTG'))
add(STEP('14.26', 'ที่ **Health checks** ตั้ง Health check grace period = **60** วินาที (รอให้เครื่องใหม่ boot เสร็จก่อนเริ่มตรวจ) '
                  'แล้วคลิก **Next**'))
add(IMG(photo('37'), 'รูปที่ 14.25 ตั้งค่า Health checks ของ ASG'))
add(BOX('**แนะนำ:** ติ๊ก **Turn on Elastic Load Balancing health checks** (Recommended) ด้วย ในแลปนี้ไม่ได้ติ๊ก (Health check type = EC2) '
        'ซึ่ง ASG จะเปลี่ยนเครื่องเฉพาะเมื่อตัวเครื่องเสีย ถ้าติ๊ก ASG จะเปลี่ยนเครื่องให้ด้วยเมื่อ**เว็บไม่ตอบ** health check ของ Load Balancer '
        '(เช่น container Nginx หยุดทำงาน)'))
add(STEP('14.27', 'Step 4 Configure group size and scaling: Desired capacity **1**, Min desired capacity **1**, Max desired capacity **2** '
                  '(เพิ่มได้สูงสุด 2 เครื่อง)'))
add(IMG(photo('38'), 'รูปที่ 14.26 ตั้งค่า Desired 1, Min 1, Max 2'))
add(BOX('**Automatic scaling:** ในแลปนี้เลือก **Target tracking scaling policy** ไว้ (Average CPU utilization, Target value 50) '
        'แต่จะแก้ค่าในส่วน I ภายหลัง ถ้าไม่ต้องการตั้งตอนนี้ให้เลือก **No scaling policies** แล้วไปสร้างในส่วน I แทนก็ได้'))
add(STEP('14.28', 'ส่วน Instance maintenance policy และ Additional settings ใช้ค่าเริ่มต้น แล้วคลิก **Next** '
                  '(Step 5 Notifications และ Step 6 Tags ข้ามได้)'))
add(IMG(photo('39'), 'รูปที่ 14.27 Instance maintenance policy และ Additional settings'))
add(STEP('14.29', 'หน้า **Review** ตรวจสอบว่า Load balancer 1 = **myLB** (Application/HTTP) Target group = **myTG**, '
                  'Health check grace period 60 seconds, Desired 1 / Min 1 / Max 2 แล้วคลิก **Create Auto Scaling group**'))
add(IMG(photo('40'), 'รูปที่ 14.28 ตรวจสอบหน้า Review'))

add(SUB('ส่วน H: ทดสอบเว็บผ่าน Load Balancer'))
add(STEP('14.30', 'ไปที่ **Target Groups** → **myTG** จะเห็นเครื่องที่ ASG สร้าง (i-097212955ba2fc5a5, us-east-1b) '
                  'ถูกลงทะเบียนเป็น target ให้อัตโนมัติ และมีสถานะ **Healthy**'))
add(IMG(photo('41'), 'รูปที่ 14.29 เครื่องจาก ASG ใน Target group'))
add(STEP('14.31', 'ที่หน้า Instances ตั้งชื่อเครื่องเป็น **Webserver1** (คลิกไอคอนดินสอในคอลัมน์ Name) จะได้ไม่สับสนเมื่อ ASG สร้างเครื่องที่สอง'))
add(IMG(photo('42'), 'รูปที่ 14.30 ตั้งชื่อ Webserver1'))
add(STEP('14.32', 'เปิด **http://44.202.88.112** (Public IP ของ Webserver1) จะเห็น **hello pageHello Sono-G** '
                  'แสดงว่า Nginx container เริ่มทำงานเองจาก AMI ตาม --restart=unless-stopped'))
add(IMG(photo('43'), 'รูปที่ 14.31 เปิดเว็บด้วย IP ของ Webserver1'))
add(STEP('14.33', f'ไปที่ **Load Balancers** → myLB (State **Active**) คัดลอก **DNS name** แล้วเปิด **http://{LB_DNS.lower()}** '
                  'จะเห็นหน้าเว็บเดียวกัน แสดงว่า Load Balancer ส่ง request ไปยังเครื่องของ ASG ได้'))
add(IMG(photo('44'), 'รูปที่ 14.32 เปิดเว็บผ่าน DNS name ของ myLB'))

add(SUB('ส่วน I: ตั้ง Dynamic scaling policy และทดสอบ Scale out'))
add(STEP('14.34', 'ไปที่ myASG → แท็บ **Automatic scaling** จะเห็น Dynamic scaling policies (1) คือ **Target Tracking Policy** ที่ Average CPU 50 '
                  'ให้คลิก **Create dynamic scaling policy**'))
add(IMG(photo('45'), 'รูปที่ 14.33 แท็บ Automatic scaling'))
add(STEP('14.35', 'ตั้งค่าแล้วคลิก **Create**'))
add(BUL('Policy type: **Target tracking scaling**'))
add(BUL('Scaling policy name: **Target Tracking Policy** (ชื่อเดิม จึง**แทนที่** policy 50% เดิม)'))
add(BUL('Metric type: **Average CPU utilization**'))
add(BUL('Target value: **1** (ถ้า CPU เฉลี่ยเกิน 1% จะเพิ่มเครื่อง)'))
add(BUL('Instance warmup: **5** วินาที'))
add(IMG(photo('46'), 'รูปที่ 14.34 ตั้ง Target value 1 เพื่อทดสอบ'))
add(BOX('**ค่านี้ใช้ทดสอบเท่านั้น:** Target value 1% ทำให้เห็นการ Scale out ได้ทันทีแม้มีงานเพียงเล็กน้อย '
        'ในการใช้งานจริงควรตั้งประมาณ **70–80%** และ Instance warmup ประมาณ 300 วินาที'))
add(STEP('14.36', 'Dynamic scaling policies ยังมี 1 รายการ แต่ตอนนี้ **Execute policy when: As required to maintain Average CPU utilization at 1** '
                  'และ Instances need 5 seconds to warm up'))
add(IMG(photo('47'), 'รูปที่ 14.35 Policy หลังแก้ไข'))
add(STEP('14.37', 'สร้างภาระให้ Webserver1 โดยเปิด Command Prompt บนคอมพิวเตอร์ของเราแล้ว ping แบบต่อเนื่อง'))
add(CODE('ping -t 44.202.88.112'))
add(P('-t ทำให้ ping ไม่หยุดจนกว่าจะกด Ctrl + C ในแลปนี้เปิดหลายหน้าต่าง (Command Prompt และ Windows PowerShell) ping พร้อมกันเพื่อเพิ่มภาระ'))
add(IMG(photo('48'), 'รูปที่ 14.36 ping Webserver1 ต่อเนื่อง'))
add(BOX('**ถ้า ping ไม่ได้ (Request timed out):** ตรวจสอบว่า Security group MySGuseast2 มี Inbound rule **All ICMP - IPv4** จาก 0.0.0.0/0 '
        'ถ้ายังไม่มีให้เพิ่ม (Ubuntu ไม่ได้บล็อก ICMP ด้วย firewall ของเครื่องเหมือน Windows)'))
add(STEP('14.38', 'รอสักครู่แล้วดูแท็บ **Activity** ของ myASG จะมีรายการใหม่ **Launching a new EC2 instance: i-0c97d06ae90036366** '
                  'สาเหตุ: CloudWatch alarm **TargetTracking-myASG-AlarmHigh-...** เข้าสถานะ **ALARM** ทำให้ policy เปลี่ยน '
                  'Desired capacity จาก **1 เป็น 2**'))
add(IMG(photo('49'), 'รูปที่ 14.37 ASG เพิ่มเครื่องเมื่อ CPU เกินเป้าหมาย'))
add(STEP('14.39', 'หน้า Instances จะมี 2 เครื่อง: Webserver1 (us-east-1b) และเครื่องใหม่ (us-east-1a, Public IP 100.48.217.55) '
                  'ซึ่ง ASG วางไว้คนละ AZ ให้อัตโนมัติ แท็บ **Monitoring** ของ Webserver1 แสดงกราฟ CPU utilization และ Network in '
                  'ที่พุ่งขึ้นช่วงที่ ping แสดงว่า Scale out ทำงานถูกต้อง'))
add(IMG(photo('50'), 'รูปที่ 14.38 มี 2 เครื่องหลัง Scale out'))
add(STEP('14.40', 'ตั้งชื่อเครื่องใหม่เป็น **Webserver2** แล้วเปิด **http://100.48.217.55** จะเห็นหน้าเว็บเดียวกัน '
                  'เครื่องใหม่ถูกเพิ่มเข้า myTG อัตโนมัติ Load Balancer จึงกระจายผู้ใช้ไปทั้ง 2 เครื่อง'))
add(IMG(photo('51'), 'รูปที่ 14.39 เปิดเว็บจาก Webserver2'))

add(SUB('ส่วน J: ทดสอบ Scale in'))
add(STEP('14.41', 'หยุด ping ทุกหน้าต่าง (Ctrl + C) จากนั้นไปที่ myASG → **Capacity overview** → **Edit** ตั้ง Desired capacity = **1** '
                  '(Min 1, Max 2 เหมือนเดิม) แล้วคลิก **Update**'))
add(IMG(photo('52'), 'รูปที่ 14.40 ลด Desired capacity เป็น 1'))
add(BOX('**ทำไมต้องลดเอง:** ในรูปที่ 14.40 Target value ของ policy เป็น **0.1** (ถูกแก้จาก 1 ระหว่างทดสอบ ภาพการแก้ไม่ได้บันทึกไว้) '
        'เป้าหมายต่ำขนาดนี้ทำให้ CPU แทบไม่ต่ำกว่าเป้า ASG จึงไม่ Scale in เอง การตั้ง Desired capacity เป็น 1 '
        'เป็นการสั่งลดเครื่องด้วยมือ ถ้าตั้ง Target value ตามปกติ (เช่น 70%) ASG จะ Scale in เองเมื่อภาระลดลง โดย scale in ช้ากว่า scale out '
        'เพื่อป้องกันการเพิ่ม/ลดเครื่องไปมา'))
add(STEP('14.42', 'แท็บ **Activity** จะมีรายการ **Terminating EC2 instance: i-0c97d06ae90036366 - Waiting For ELB Connection Draining** '
                  'สถานะ **Connection draining in progress** สาเหตุ: user request เปลี่ยน Desired capacity จาก 2 เป็น 1'))
add(IMG(photo('53'), 'รูปที่ 14.41 ASG ลบเครื่องเมื่อ Scale in'))
add(BOX('**Connection draining:** ก่อนลบเครื่อง Load Balancer จะหยุดส่ง request ใหม่ไปที่เครื่องนั้น และรอให้ request ที่ค้างอยู่ทำงานเสร็จ '
        '(ค่าเริ่มต้นสูงสุด 300 วินาที) ผู้ใช้ที่กำลังใช้งานจึงไม่ถูกตัดกลางคัน'))

add(SUB('ส่วน K: คืนทรัพยากร (Clean up)'))
add(STEP('14.43', 'เมื่อทำเสร็จ ให้ลบทรัพยากรตามลำดับนี้', keep_next=False))
add(BUL('Auto Scaling Groups → myASG → Actions → **Delete** (เครื่อง Webserver ทั้งหมดจะถูกลบตาม)'))
add(BUL('Load Balancers → myLB → **Delete load balancer** แล้ว Target Groups → myTG → **Delete**'))
add(BUL('Launch Templates → myLT → **Delete template**'))
add(BUL('AMIs → myAMI → **Deregister AMI** แล้วลบ Snapshot ของ AMI'))
add(BUL('ถ้าไม่ใช้แล้ว ลบ Inbound rule SSH ออกจาก MySGuseast2'))

# =====================================================================
# 15. CloudWatch (no photos yet)
# =====================================================================
add(H('15. CloudWatch'))
add(SUB('วัตถุประสงค์'))
add(P('**Amazon CloudWatch** คือบริการติดตามการทำงาน (Monitoring) ของ AWS เก็บค่าตัวเลขของทรัพยากร (**Metrics**) เช่น การใช้ CPU, '
      'ปริมาณข้อมูลเข้า-ออกเครือข่าย, การอ่าน-เขียนดิสก์ ของ EC2 ทุกเครื่องโดยอัตโนมัติ (ค่าเริ่มต้นเก็บทุก 5 นาที) '
      'เราใช้ CloudWatch ทำได้ 3 อย่างหลักในหัวข้อนี้'))
add(BUL('**Metrics** – ดูค่าและกราฟของ metric ย้อนหลัง'))
add(BUL('**Alarms** – ตั้งเงื่อนไข เช่น CPU เกินค่าที่กำหนด แล้วให้ส่งอีเมลแจ้งเตือนผ่าน **Amazon SNS (Simple Notification Service)**'))
add(BUL('**Dashboards** – รวมกราฟหลายตัวไว้ในหน้าเดียว เพื่อดูสถานะของระบบได้ทันที'))
add(BOX('**ความเชื่อมโยงกับหัวข้อที่ 14:** Target tracking scaling policy ของ Auto Scaling ก็ทำงานผ่าน CloudWatch alarm '
        '(TargetTracking-myASG-AlarmHigh-...) ที่ AWS สร้างให้อัตโนมัติ ในหัวข้อนี้เราจะสร้าง Alarm เองด้วยมือ'))
add(TABLE(['ทรัพยากร', 'ชื่อ', 'ค่าที่ใช้'],
          [['EC2 ที่ติดตาม', 'i-0a5e590df3ec102c8', 'm7i-flex.large, us-east-1c, Public IP 174.129.187.183'],
           ['SNS topic', 'Web_Server_Overloading', 'ส่งอีเมลไปยังอีเมลของเรา'],
           ['Alarm', 'myAlarm', 'CPUUtilization (Average, 5 นาที) > 0.1'],
           ['Dashboard', 'SOC', 'CPUUtilization (Line), NetworkIn และ NetworkOut (Number)']],
          [2200, 2600, 4200]))

add(SUB('ส่วน A: ดู Metrics ของเครื่อง EC2'))
add(STEP('15.1', 'พิมพ์ **CloudWatch** ในช่อง Search แล้วเลือกบริการ CloudWatch จะเข้าสู่หน้า **Overview** '
                 'ซึ่งตอนนี้ยังไม่มี alarm, metric หรือ dashboard ที่ตั้งไว้ เมนูด้านซ้ายมี Dashboards, Alarms และ Metrics ที่จะใช้ในหัวข้อนี้'))
add(IMG(photo('54'), 'รูปที่ 15.1 หน้า Overview ของ CloudWatch'))
add(STEP('15.2', 'สร้างเครื่อง EC2 สำหรับทดสอบ (ในแลปนี้เป็น Windows Server ที่เชื่อมต่อด้วย RDP ได้ ใช้ m7i-flex.large, Key pair MyKPuseast2, '
                 'Security group MySGuseast2 เหมือน Part 1 หัวข้อที่ 3 ภาพหน้าตั้งค่าไม่ได้บันทึกไว้) '
                 'จด **Instance ID** ไว้ (ในแลปนี้คือ **i-0a5e590df3ec102c8**) แท็บ Monitoring ของเครื่องใหม่จะยังแสดง **No data available** '
                 'ต้องรอสักครู่ให้ CloudWatch เก็บข้อมูล'))
add(IMG(photo('55'), 'รูปที่ 15.2 เครื่อง EC2 ที่จะติดตาม'))
add(STEP('15.3', 'ไปที่ CloudWatch → **Metrics** → **Classic metrics** แท็บ **Browse** เลือก **EC2** → **Per-Instance Metrics** '
                 'แล้ววาง Instance ID ในช่องค้นหา จะพบ metric ของเครื่องนี้ 18 รายการ ติ๊ก **CPUUtilization** '
                 'กราฟด้านบนจะแสดงการใช้ CPU เป็นเปอร์เซ็นต์ ปรับช่วงเวลาได้ที่ 1h / 3h / 12h / 1d ...'))
add(IMG(photo('56'), 'รูปที่ 15.3 ค้นหา metric ด้วย Instance ID'))
add(TABLE(['Metric', 'ความหมาย'],
          [['CPUUtilization', 'เปอร์เซ็นต์การใช้ CPU'],
           ['NetworkIn / NetworkOut', 'จำนวน byte ที่รับเข้า / ส่งออกทางเครือข่าย'],
           ['NetworkPacketsIn / NetworkPacketsOut', 'จำนวน packet ที่รับเข้า / ส่งออก'],
           ['EBSReadBytes / EBSWriteBytes', 'จำนวน byte ที่อ่าน / เขียนดิสก์ EBS'],
           ['StatusCheckFailed', 'ผลตรวจสุขภาพเครื่อง (0 = ปกติ, 1 = มีปัญหา)']],
          [3600, 5400]))
add(STEP('15.4', 'ติ๊กหลาย metric พร้อมกันได้ ในแลปนี้เลือก **CPUUtilization, NetworkIn และ NetworkOut** (แท็บ Graphed metrics (3)) '
                 'แล้วเปลี่ยนรูปแบบการแสดงผลจาก **Line** เป็น **Gauge** ที่มุมขวาบน จะเห็นค่าล่าสุด เช่น CPU **2.78%**, '
                 'NetworkIn **637 byte**, NetworkOut **526 byte** ในรูปนี้ยังเปิด RDP เข้าเครื่องและเปิดหน้าเว็บที่มีภาพเคลื่อนไหว '
                 'เพื่อให้เครื่องมีการใช้ CPU และเครือข่าย'))
add(IMG(photo('57'), 'รูปที่ 15.4 แสดงหลาย metric แบบ Gauge'))
add(BOX('**ข้อความสีแดง "You have to set the gauge range":** กราฟแบบ Gauge ต้องกำหนดค่าต่ำสุด-สูงสุดของหน้าปัด '
        'ที่แท็บ **Options** (เช่น CPU 0–100) ถ้าไม่ตั้ง หน้าปัดจะแสดงตัวเลขอย่างเดียว'))

add(SUB('ส่วน B: สร้าง Alarm ที่ส่งอีเมลแจ้งเตือน'))
add(STEP('15.5', 'ไปที่ CloudWatch → **Alarms** (ตอนนี้ Alarms (0)) แล้วคลิก **Create alarm**'))
add(IMG(photo('58'), 'รูปที่ 15.5 หน้า Alarms'))
add(STEP('15.6', 'คลิก **Select metric** → **EC2** → **Per-Instance Metrics** ค้นหาด้วย Instance ID '
                 '(i-0a5e590df3ec102c8) ติ๊ก **CPUUtilization** แล้วคลิก **Select metric**'))
add(IMG(photo('59'), 'รูปที่ 15.6 เลือก metric CPUUtilization'))
add(STEP('15.7', 'Step 1 **Specify metric and conditions** ตั้งค่าดังนี้ แล้วคลิก **Next**'))
add(BUL('Data source: **Metrics**, Type: **Classic**'))
add(BUL('Metric: Namespace **AWS/EC2**, Metric name **CPUUtilization**, InstanceId **i-0a5e590df3ec102c8**'))
add(BUL('Statistic: **Average**, Period: **5 minutes**'))
add(BUL('Threshold type: **Static** (ใช้ตัวเลขคงที่)'))
add(BUL('Whenever CPUUtilization is: **Greater (> threshold)** than **0.1**'))
add(BUL('Additional configuration: Datapoints to alarm **1 out of 1**, Missing data treatment **Treat missing data as missing**'))
add(P('ความหมาย: ถ้าค่าเฉลี่ย CPU ในช่วง 5 นาทีใดๆ มากกว่า 0.1% เพียง 1 ครั้ง Alarm จะเข้าสถานะ **ALARM** '
      '(ในกราฟ Preview คือเมื่อเส้นสีน้ำเงินสูงกว่าเส้นสีแดง)'))
add(IMG(photo('60'), 'รูปที่ 15.7 ตั้งเงื่อนไข CPUUtilization > 0.1'))
add(BOX('**ค่า 0.1% ใช้ทดสอบเท่านั้น:** ตั้งต่ำมากเพื่อให้ Alarm ทำงานทันทีและเห็นอีเมลแจ้งเตือน '
        'ในการใช้งานจริงควรตั้งประมาณ **80%** และใช้ Datapoints เช่น 3 out of 3 เพื่อไม่ให้แจ้งเตือนจากการใช้ CPU สูงเพียงชั่วครู่'))
add(STEP('15.8', 'Step 2 **Configure actions** ส่วน Notification ตั้งค่าดังนี้ แล้วคลิก **Next**'))
add(BUL('Alarm state trigger: **In alarm** (แจ้งเตือนเมื่อเข้าสถานะ ALARM)'))
add(BUL('Send a notification to the following SNS topic: ครั้งแรกเลือก **Create new topic** ตั้งชื่อ **Web_Server_Overloading** '
        'ใส่ **อีเมลของเรา** ในช่อง Email endpoints แล้วคลิก **Create topic** '
        '(ในรูปสร้างไว้แล้ว จึงแสดงเป็น Select an existing SNS topic → Web_Server_Overloading)'))
add(BUL('Lambda action, Auto Scaling action, EC2 action และ Systems Manager action: ไม่ต้องใช้'))
add(IMG(photo('61'), 'รูปที่ 15.8 ตั้งค่า Notification ไปยัง SNS topic'))
add(STEP('15.9', 'เปิดอีเมลของเรา จะได้รับอีเมล **AWS Notification - Subscription Confirmation** จาก no-reply@sns.amazonaws.com '
                 'แจ้งว่าเราสมัครรับข่าวจาก topic arn:aws:sns:us-east-1:...:Web_Server_Overloading ให้คลิก **Confirm subscription**'))
add(IMG(photo('62'), 'รูปที่ 15.9 อีเมลยืนยันการสมัครรับการแจ้งเตือน'))
add(STEP('15.10', 'จะเปิดหน้า **Subscription confirmed!** แปลว่ายืนยันสำเร็จ ต่อจากนี้อีเมลนี้จะได้รับการแจ้งเตือนจาก topic'))
add(IMG(photo('63'), 'รูปที่ 15.10 ยืนยันการสมัครสำเร็จ'))
add(BOX('**ต้องยืนยันอีเมลก่อน:** ถ้าไม่คลิก Confirm subscription สถานะ subscription จะเป็น Pending confirmation '
        'และจะ**ไม่ได้รับอีเมลแจ้งเตือน** ถ้าไม่เห็นอีเมลให้ดูในโฟลเดอร์ Spam หรือ Promotions'))
add(STEP('15.11', 'Step 3 **Add alarm details** ตั้ง Alarm name = **myAlarm** (Alarm description ไม่บังคับ) แล้วคลิก **Next**'))
add(IMG(photo('64'), 'รูปที่ 15.11 ตั้งชื่อ myAlarm'))
add(STEP('15.12', 'Step 4 **Preview and create** ตรวจสอบเงื่อนไข (CPUUtilization Greater (>) than 0.1) Action '
                  '(When In alarm, send a notification to "Web_Server_Overloading") และชื่อ myAlarm แล้วคลิก **Create alarm**'))
add(IMG(photo('65'), 'รูปที่ 15.12 ตรวจสอบแล้ว Create alarm'))
add(STEP('15.13', 'Alarm จะเริ่มที่สถานะ **Insufficient data** (ยังมีข้อมูลไม่พอ) เมื่อ CPU เกิน 0.1% จะเปลี่ยนเป็น **In alarm** '
                  'และส่งอีเมลหัวข้อ **ALARM: "myAlarm" in US East (N. Virginia)** ซึ่งบอกรายละเอียด เช่น'))
add(BUL('State Change: **INSUFFICIENT_DATA → ALARM**'))
add(BUL('Reason: Threshold Crossed: 1 out of the last 1 datapoints **[59.52...]** was greater than the threshold **(0.1)** '
        '(CPU เฉลี่ยขณะนั้นประมาณ 59.5%)'))
add(BUL('Monitored Metric: AWS/EC2 CPUUtilization ของ InstanceId i-0a5e590df3ec102c8, Period 300 seconds, Average'))
add(IMG(photo('66'), 'รูปที่ 15.13 อีเมลแจ้งเตือนเมื่อ Alarm ทำงาน'))
add(BOX('**สถานะของ Alarm มี 3 แบบ:** **OK** (อยู่ในเกณฑ์), **In alarm** (เกินเกณฑ์) และ **Insufficient data** (ข้อมูลไม่พอ) '
        'ในขั้นตอนที่ 15.8 เลือกแจ้งเตือนเฉพาะ In alarm ถ้าต้องการรู้ด้วยว่าระบบกลับมาปกติ ให้คลิก Add notification เพิ่ม trigger **OK**'))

add(SUB('ส่วน C: สร้าง Dashboard'))
add(STEP('15.14', 'ไปที่ CloudWatch → **Dashboards** แท็บ **Custom Dashboards** (ตอนนี้ยังไม่มี) แล้วคลิก **Create dashboard** '
                  '(สังเกตว่าเมนู Alarms ด้านซ้ายแสดง ⚠ 1 คือมี 1 alarm อยู่ในสถานะ In alarm)'))
add(IMG(photo('67'), 'รูปที่ 15.14 หน้า Custom Dashboards'))
add(STEP('15.15', 'ตั้ง Dashboard name = **SOC** (ใช้ได้เฉพาะ 0-9 A-Z a-z - _) แล้วคลิก **Create dashboard**'))
add(IMG(photo('68'), 'รูปที่ 15.15 ตั้งชื่อ Dashboard'))
add(STEP('15.16', 'หน้าต่าง **Add widget** จะเปิดขึ้น เลือก Data sources types **Cloudwatch**, Data type **Metrics**, '
                  'Preferred experience **Metrics Console** และ Widget type ตามต้องการ (เช่น **Line** สำหรับกราฟตามเวลา, '
                  '**Number** สำหรับค่าล่าสุด, **Gauge** สำหรับหน้าปัด) แล้วคลิก **Next**'))
add(IMG(photo('69'), 'รูปที่ 15.16 เลือกชนิด widget'))
add(STEP('15.17', 'หน้า **Add metric graph** ค้นหาด้วย Instance ID ใน EC2 → Per-Instance Metrics ติ๊ก metric ที่ต้องการ (เช่น **CPUUtilization**) '
                  'แล้วคลิก **Create widget** ทำซ้ำด้วยปุ่ม **+** มุมขวาบนเพื่อเพิ่ม widget อื่น'))
add(IMG(photo('70'), 'รูปที่ 15.17 เลือก metric สำหรับ widget'))
add(STEP('15.18', 'Dashboard **SOC** ในแลปนี้มี 3 widget คือ **CPUUtilization** (Line), **NetworkIn** และ **NetworkOut** (Number) '
                  'แล้ว**คลิก Save** ที่มุมขวาบน'))
add(IMG(photo('71'), 'รูปที่ 15.18 ตัวอย่าง Dashboard SOC'))
add(BOX('**อย่าลืมกด Save:** มุมขวาบนแสดง **Autosave: Off** ถ้าไม่กด Save แล้วออกจากหน้า widget ที่เพิ่มจะหายทั้งหมด'))

add(SUB('ส่วน D: คืนทรัพยากร (Clean up)'))
add(STEP('15.19', 'เมื่อทำเสร็จ ให้ลบทรัพยากรเพื่อไม่ให้เสีย credit และไม่ได้รับอีเมลแจ้งเตือนต่อ', keep_next=False))
add(BUL('CloudWatch → Alarms → myAlarm → Actions → **Delete**'))
add(BUL('CloudWatch → Dashboards → SOC → **Delete**'))
add(BUL('Amazon SNS → Topics → Web_Server_Overloading → **Delete** (หรือคลิกลิงก์ unsubscribe ท้ายอีเมลแจ้งเตือน)'))
add(BUL('EC2 → Terminate เครื่อง i-0a5e590df3ec102c8'))

# ---------- Summary ----------
add(H('สรุป Part 5'))
add(SUB('ค่าที่ใช้ในแลปนี้ (ใช้อ้างอิงเมื่อทำซ้ำ)'))
add(TABLE(['รายการ', 'ค่าที่ใช้', 'หมายเหตุ'],
          [['Launch template (หัวข้อ 13)', 'myLT (lt-0e04c8a87597c1ac4)', 'Amazon Linux 2023, m7i-flex.large, ไม่มี Key pair, MySGuseast2'],
           ['ASG (หัวข้อ 13)', 'myASG', 'Desired/Min/Max = 1, us-east-1a, ไม่มี Load Balancer'],
           ['เครื่องต้นแบบ', 'i-028ffde8c374c7aa1', 'Ubuntu 26.04, Docker + Nginx (my-nginx), us-east-1c'],
           ['AMI', 'myAMI (ami-093a1cd621d9a1b12)', '8 GiB gp3'],
           ['Load balancer', 'myLB', f'Application, Internet-facing, us-east-1a + us-east-1b, {LB_DNS}'],
           ['Target group', 'myTG', 'HTTP:80, Healthy 2, Unhealthy 2, Timeout 14 s, Interval 15 s, Success 200-499'],
           ['Launch template (หัวข้อ 14)', 'myLT (lt-0134575efc5229034)', 'myAMI, m7i-flex.large, MyKPuseast2, MySGuseast2'],
           ['ASG (หัวข้อ 14)', 'myASG', 'Desired 1, Min 1, Max 2, us-east-1a + us-east-1b, myTG, grace period 60 s'],
           ['Scaling policy', 'Target Tracking Policy', 'Average CPU utilization, Target 1 (ทดสอบ), warmup 5 s'],
           ['Webserver1', 'i-097212955ba2fc5a5', 'us-east-1b, 44.202.88.112'],
           ['Webserver2', 'i-0c97d06ae90036366', 'us-east-1a, 100.48.217.55 (สร้างตอน Scale out)'],
           ['เครื่องที่ติดตาม (หัวข้อ 15)', 'i-0a5e590df3ec102c8', 'm7i-flex.large, us-east-1c, 174.129.187.183'],
           ['SNS topic', 'Web_Server_Overloading', 'Email subscription ที่ยืนยันแล้ว'],
           ['CloudWatch alarm', 'myAlarm', 'CPUUtilization Average 5 นาที > 0.1 (1 out of 1) → แจ้งเตือนเมื่อ In alarm'],
           ['CloudWatch dashboard', 'SOC', 'CPUUtilization (Line), NetworkIn, NetworkOut (Number)']],
          [2600, 3200, 3200]))
add(SUB('สิ่งที่ควรจำจาก Part 5'))
add(BUL('Auto Scaling group รักษาจำนวนเครื่องให้เท่ากับ Desired capacity เสมอ ถ้าเครื่องถูกลบหรือเสีย จะสร้างเครื่องใหม่แทน'))
add(BUL('Launch template ไม่ควรระบุ Subnet เพื่อให้ ASG กระจายเครื่องไปหลาย AZ ได้'))
add(BUL('Web server ที่จะใช้กับ Auto Scaling ต้องเริ่มให้บริการเองเมื่อเปิดเครื่อง (เช่น docker --restart=unless-stopped หรือ Apache เป็น service)'))
add(BUL('ASG ที่ผูกกับ Target group จะลงทะเบียนและถอนเครื่องออกจาก Load Balancer ให้อัตโนมัติ และ AZ ของ ASG ควรตรงกับ Load Balancer'))
add(BUL('Target tracking policy ใช้ CloudWatch alarm ตรวจ metric (เช่น CPU) แล้วปรับ Desired capacity ภายในช่วง Min–Max'))
add(BUL('ค่าที่ใช้ทดสอบ (Target 1%, warmup 5 วินาที) ไม่เหมาะกับงานจริง ควรใช้ประมาณ 70–80% และ warmup ประมาณ 300 วินาที'))
add(BUL('ลบเครื่องของ ASG ต้องลบที่ ASG ไม่ใช่ Terminate เครื่องโดยตรง'))
add(BUL('CloudWatch เก็บ metric ของ EC2 ให้อัตโนมัติ (CPU, Network, EBS, Status check) ค้นหาได้ด้วย Instance ID'))
add(BUL('Alarm ส่งอีเมลผ่าน SNS topic และต้องคลิก Confirm subscription ในอีเมลก่อนจึงจะได้รับการแจ้งเตือน'))
add(BUL('Alarm มี 3 สถานะ OK / In alarm / Insufficient data และค่าทดสอบ (> 0.1%) ควรเปลี่ยนเป็นประมาณ 80% ในงานจริง'))
add(BUL('Dashboard รวมกราฟหลาย metric ไว้ในหน้าเดียว และต้องกด Save เพราะ Autosave ปิดอยู่'))
add(PAGEBREAK())

splice_part(UN, 5, ''.join(X), IMG)
