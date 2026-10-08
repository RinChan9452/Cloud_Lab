"""Part 4 content (Thai). Usage: python build_part4.py <unpacked_docx_dir> "D:/Cloud lab/Part 4" """
import sys
from report_lib import H, SUB, P, STEP, BUL, BOX, CODE, TABLE, PAGEBREAK, Images, load_photos, splice_part

UN, PHOTOS = sys.argv[1], sys.argv[2]
photos = load_photos(PHOTOS)
def photo(key, idx=0):
    return photos[key][idx]
IMG = Images(UN, 'part4', docpr_base=4000)

X = []
add = X.append

ENDPOINT = 'mysqlinstance.c2d9ff9pc5yb.us-east-1.rds.amazonaws.com'
LB_DNS = 'myLB-1498070466.us-east-1.elb.amazonaws.com'

# ---------- Intro ----------
add(P('Part 4 เป็นการเรียนรู้บริการฐานข้อมูลแบบ Managed และตัวกระจายโหลด (Load Balancer) ของ AWS ประกอบด้วย 2 แลปที่ต่อเนื่องกัน'))
add(BUL('**Relational DB Service (RDS)** – สร้างฐานข้อมูล MySQL บน Amazon RDS แล้วสร้าง EC2 ที่ติดตั้ง XAMPP (Apache, PHP, '
        'phpMyAdmin) ให้เชื่อมต่อกับฐานข้อมูลนั้น พร้อมทำหน้าเว็บ test.php ที่อ่านข้อมูลจาก RDS'))
add(BUL('**Elastic Load Balancer (ELB)** – สร้าง AMI จาก Web server ในหัวข้อที่ 11 เพื่อได้เครื่องที่สองคนละ Availability Zone '
        'แล้วสร้าง Application Load Balancer กระจายผู้ใช้ไปยังทั้งสองเครื่อง'))
add(BOX('**ก่อนเริ่ม:** ทุกขั้นตอนทำใน Region **United States (N. Virginia) us-east-1** และใช้ Key pair **MyKPuseast2** '
        'กับ Security Group **MySGuseast2** จาก Part 1 หัวข้อที่ 12 ต้องใช้ทรัพยากรจากหัวข้อที่ 11 จึง**ยังไม่ต้องลบอะไร**จนกว่าจะจบ Part 4'))

# =====================================================================
# 11. RDS
# =====================================================================
add(H('11. Relational DB Service (RDS)'))
add(SUB('วัตถุประสงค์'))
add(P('**Amazon RDS (Relational Database Service)** คือบริการฐานข้อมูลเชิงสัมพันธ์แบบ **Managed service** ที่ AWS ดูแลเครื่อง '
      'ระบบปฏิบัติการ การติดตั้งซอฟต์แวร์ฐานข้อมูล การสำรองข้อมูลอัตโนมัติ และการอัปเดตให้ เราแค่เลือก Engine (เช่น MySQL) '
      'ขนาดเครื่อง และนำ **Endpoint** ไปเชื่อมต่อ ต่างจาก Part 1 หัวข้อที่ 4 ที่ติดตั้ง MySQL ใน XAMPP เองบน EC2 (Self-managed)'))
add(P('เมื่อแยกฐานข้อมูลออกมาไว้ที่ RDS แล้ว Web server จะไม่ต้องเก็บข้อมูลไว้ในเครื่อง จึงสร้าง Web server หลายเครื่องที่ใช้ฐานข้อมูลเดียวกันได้ '
      '(ใช้ในหัวข้อที่ 12)'))
add(TABLE(['ทรัพยากร', 'ชื่อ', 'ค่าที่ใช้'],
          [['ฐานข้อมูล RDS', 'mysqlinstance', 'MySQL Community 8.4.9, db.t3.micro, Single-AZ, us-east-1c'],
           ['Database ใน RDS', 'myDB', 'Master username mysqlAdmin, Port 3306'],
           ['Security group ของ RDS', 'mySQLinstance', 'Inbound MYSQL/Aurora TCP 3306'],
           ['Web server (EC2)', 'myWebAppServer', 'Windows Server 2025, m7i-flex.large, us-east-1c'],
           ['ซอฟต์แวร์บน EC2', 'XAMPP', 'Apache + PHP + phpMyAdmin (ไม่ติดตั้ง MySQL)']],
          [2400, 2200, 4400]))

add(SUB('ส่วน A: สร้างฐานข้อมูล MySQL บน RDS'))
add(STEP('11.1', 'พิมพ์ **RDS** ในช่อง Search แล้วเลือกบริการ **Aurora and RDS** จะเข้าสู่หน้า Dashboard ซึ่งแสดงว่ายังไม่มีฐานข้อมูล '
                 '(DB instances = 0)'))
add(IMG(photo('1'), 'รูปที่ 11.1 หน้า Dashboard ของ Aurora and RDS'))
add(STEP('11.2', 'คลิกปุ่ม **Create** ใต้หัวข้อ **Create with full configuration** (ปุ่มสีขาวด้านขวา) '
                 '**ไม่ใช่**ปุ่ม Create สีส้มด้านซ้าย เพราะปุ่มสีส้มเป็น Express configuration ที่สร้าง Aurora PostgreSQL ให้อัตโนมัติ'))
add(IMG(photo('2'), 'รูปที่ 11.2 เลือก Create with full configuration'))
add(STEP('11.3', 'ตั้งค่าส่วนแรก'))
add(BUL('Engine type: **MySQL**'))
add(BUL('Choose a database creation method: **Full configuration** (ตั้งค่าเองทุกอย่าง)'))
add(BUL('Templates: **Dev/Test**'))
add(IMG(photo('3'), 'รูปที่ 11.3 เลือก MySQL, Full configuration และ Dev/Test'))
add(STEP('11.4', 'ตั้งค่า Availability and durability และ Settings'))
add(BUL('Deployment options: **Single-AZ DB instance deployment (1 instance)** (Template Dev/Test จะเลือก Multi-AZ 2 instances ไว้ '
        'ต้องเปลี่ยนเอง Single-AZ ถูกที่สุด แต่ไม่มีเครื่องสำรอง)'))
add(BUL('Edition: **MySQL Community**'))
add(BUL('Engine version: **MySQL 8.4.9**'))
add(BUL('DB instance identifier: **mysqlInstance** (AWS จะเก็บเป็นตัวพิมพ์เล็ก mysqlinstance)'))
add(IMG(photo('4'), 'รูปที่ 11.4 เลือก Single-AZ และตั้งชื่อ DB instance'))
add(STEP('11.5', 'ตั้งค่า Credentials และ Instance configuration'))
add(BUL('Master username: **mysqlAdmin** (ชื่อผู้ใช้หลักของฐานข้อมูล ใช้แทน root)'))
add(BUL('Credentials management: **Self managed**'))
add(BUL('Auto generate password: **ไม่ต้องติ๊ก** แล้วพิมพ์ Master password และ Confirm master password เอง '
        '(อย่างน้อย 8 ตัว ห้ามมี / \' " @)'))
add(BUL('Database authentication: **Password authentication**'))
add(BUL('DB instance class: เปิด **Include previous generation classes** → **Burstable classes (includes t classes)** → **db.t3.micro** '
        '(2 vCPU, 1 GiB RAM)'))
add(IMG(photo('5'), 'รูปที่ 11.5 ตั้งค่า Master username, password และ db.t3.micro'))
add(BOX('**จดรหัสผ่านไว้:** Master username และ Master password จะใช้อีกครั้งในขั้นตอนที่ 11.23 และ 11.33 '
        'ถ้าลืมต้องไป Modify ฐานข้อมูลเพื่อตั้งรหัสใหม่'))
add(STEP('11.6', 'ตั้งค่า Storage และ Connectivity'))
add(BUL('Storage type: **General Purpose SSD (gp3)**'))
add(BUL('Allocated storage: **100** GiB หรือน้อยกว่า (ค่าเริ่มต้นคือ 200 ต้องแก้ ดูขั้นตอนที่ 11.11)'))
add(BUL('Compute resource: **Don\'t connect to an EC2 compute resource**'))
add(BUL('Virtual private cloud (VPC): **Default VPC (vpc-0ab1645036dc923b6)** (เปลี่ยนภายหลังไม่ได้)'))
add(BUL('DB subnet group: **default-vpc-0ab1645036dc923b6**'))
add(IMG(photo('6'), 'รูปที่ 11.6 ตั้งค่า Storage และ VPC (ในรูปยังเป็น 200 GiB)'))
add(STEP('11.7', 'ตั้งค่าส่วนที่เหลือของ Connectivity'))
add(BUL('Public access: **Yes** (ให้ฐานข้อมูลมี Public IP เชื่อมต่อจากนอก VPC ได้)'))
add(BUL('VPC security group (firewall): **Create new** → ชื่อ **mySQLinstance**'))
add(BUL('Availability Zone: **No preference** (AWS เลือกให้ ในแลปนี้ได้ us-east-1c)'))
add(BUL('Create an RDS Proxy: ไม่ต้องติ๊ก, Certificate authority: ใช้ค่าเริ่มต้น'))
add(IMG(photo('7'), 'รูปที่ 11.7 เปิด Public access และสร้าง Security group ใหม่'))
add(STEP('11.8', 'Monitoring: เลือก **Database Insights - Standard** และ**ไม่ต้องติ๊ก Enable Enhanced monitoring** เพราะทำให้เสีย credit เร็วขึ้น '
                 'Log exports ไม่ต้องเลือก'))
add(IMG(photo('8'), 'รูปที่ 11.8 ตั้งค่า Monitoring'))
add(STEP('11.9', 'เปิด **Additional configuration** แล้วตั้ง **Initial database name** = **myDB** '
                 '(ถ้าเว้นว่าง RDS จะไม่สร้าง database ให้) ส่วน DB parameter group, Option group, Encryption และ Backup '
                 '(เก็บ 7 วัน) ใช้ค่าเริ่มต้น'))
add(IMG(photo('9'), 'รูปที่ 11.9 ตั้งชื่อ Initial database name เป็น myDB'))
add(STEP('11.10', 'Maintenance ใช้ค่าเริ่มต้น และ**ไม่ต้องติ๊ก Enable deletion protection** (เพื่อให้ลบฐานข้อมูลได้หลังทำแลป) '
                  'แล้วคลิก **Create database**'))
add(IMG(photo('10'), 'รูปที่ 11.10 คลิก Create database'))
add(STEP('11.11', 'ถ้าใช้ Allocated storage 200 GiB ตามค่าเริ่มต้น จะขึ้น error สีแดง **Your request to create DB instance mysqlInstance didn\'t work** '
                  '... **not authorized to perform: rds:CreateDBInstance ... with an explicit deny** เพราะบัญชี AWS Academy '
                  'จำกัดไม่ให้สร้าง storage เกิน 100 GB ให้กลับไปแก้ **Allocated storage เป็น 100** แล้วคลิก Create database อีกครั้ง'))
add(IMG(photo('11'), 'รูปที่ 11.11 Error เมื่อใช้ storage 200 GiB'))
add(STEP('11.12', 'หน้า **Databases** จะแสดง **mysqlinstance** สถานะ **Creating** (db.t3.micro, MySQL Community, Default VPC) '
                  'ให้รอจนสถานะเป็น **Available**'))
add(IMG(photo('12'), 'รูปที่ 11.12 ฐานข้อมูลกำลังสร้าง (Creating)'))
add(BOX('**เวลารอ:** การสร้าง RDS ใช้เวลาประมาณ 10 นาทีขึ้นไป (Creating → Backing-up → Available) '
        'ระหว่างรอให้ทำส่วน B และ C (สร้าง EC2 และติดตั้ง XAMPP) ไปก่อนได้'))

add(SUB('ส่วน B: สร้าง EC2 สำหรับ Web server'))
add(STEP('11.13', 'คลิกที่ชื่อ **mysqlinstance** → แท็บ **Connectivity & security** แล้วดูหัวข้อ Networking ว่าฐานข้อมูลอยู่ '
                  '**Availability Zone us-east-1c** และ **VPC vpc-0ab1645036dc923b6** เพื่อนำไปตั้งค่า EC2 ให้ตรงกัน '
                  'หน้านี้ยังแสดง Database name **myDB**, Master username **mysqlAdmin**, Port **3306** '
                  'และ VPC security group **mySQLinstance (sg-0da62f55a8f532e78)**'))
add(IMG(photo('14'), 'รูปที่ 11.13 ตรวจสอบ VPC และ Availability Zone ของฐานข้อมูล'))
add(STEP('11.14', 'ไปที่ EC2 → **Launch instances** แล้วสร้างเครื่องเหมือน Part 1 หัวข้อที่ 3 โดยตั้งค่าดังนี้'))
add(BUL('Name: **myWebAppServer**'))
add(BUL('AMI: **Microsoft Windows Server 2025 Base**, Instance type: **m7i-flex.large**'))
add(BUL('Key pair: **MyKPuseast2**'))
add(BUL('VPC: **Default VPC (vpc-0ab1645036dc923b6)** เดียวกับฐานข้อมูล, Subnet: **No preference**'))
add(BUL('Availability Zone: **us-east-1c** (ตรงกับฐานข้อมูล)'))
add(BUL('Auto-assign public IP: **Enable**'))
add(BUL('Firewall: **Select existing security group** → **MySGuseast2**'))
add(BUL('Storage: **30 GiB gp3**'))
add(IMG(photo('13'), 'รูปที่ 11.14 สร้าง EC2 ใน VPC และ AZ เดียวกับฐานข้อมูล'))
add(BOX('**ทำไมต้องอยู่ VPC และ AZ เดียวกัน:** เครื่องใน VPC เดียวกันจะคุยกับฐานข้อมูลผ่าน Private IP ภายในเครือข่ายของ AWS ได้ '
        'ส่วนการอยู่ AZ เดียวกันช่วยให้ latency ต่ำและไม่มีค่าโอนข้อมูลข้าม AZ'))
add(STEP('11.15', 'หน้า Instances จะเห็น **myWebAppServer** (i-074f2a7d199174feb) ที่ us-east-1c ให้จด **Private IPv4 address** '
                  '(**172.31.20.89**) ไว้ จะใช้ตรวจสอบในขั้นตอนที่ 11.27'))
add(IMG(photo('15'), 'รูปที่ 11.15 Instance myWebAppServer'))

add(SUB('ส่วน C: ติดตั้ง XAMPP บน EC2 (ไม่ติดตั้ง MySQL)'))
add(STEP('11.16', 'เชื่อมต่อ RDP เข้า myWebAppServer (Connect → แท็บ RDP → Download RDP shortcut file → Get Windows password ด้วย '
                  'MyKPuseast2.pem) เหมือน Part 1 ขั้นตอนที่ 3.7–3.16'))
add(IMG(photo('16'), 'รูปที่ 11.16 เชื่อมต่อ Remote Desktop เข้า myWebAppServer'))
add(STEP('11.17', 'ในเครื่อง EC2 เปิด **Windows Security** → **Firewall & network protection** แล้วปิด Firewall ของ '
                  '**Private network** และ **Public network** เหมือน Part 1 ขั้นตอนที่ 4.1'))
add(IMG(photo('17'), 'รูปที่ 11.17 ปิด Windows Firewall'))
add(STEP('11.18', 'ดาวน์โหลด XAMPP for Windows (เหมือน Part 1 ขั้นตอนที่ 4.2) แล้วติดตั้ง ในหน้า **Select Components** '
                  '**เอาเครื่องหมายออกจาก MySQL** เพราะฐานข้อมูลอยู่ที่ RDS แล้ว ให้เลือกเฉพาะ **Apache, PHP และ phpMyAdmin** '
                  '(FileZilla, Mercury, Tomcat, Perl, Webalizer, Fake Sendmail ไม่ต้องเลือก)'))
add(IMG(photo('18'), 'รูปที่ 11.18 เลือก Components โดยไม่ติดตั้ง MySQL'))
add(STEP('11.19', 'เปิด **XAMPP Control Panel** แล้ว**ติ๊กช่องในคอลัมน์ Service หน้า Apache** → ยืนยันให้ติดตั้งเป็น Windows service '
                  '(log จะขึ้น Installing service... Successful!) จากนั้นคลิก **Start** ที่ Apache '
                  'การติดตั้งเป็น service ทำให้ **Apache เริ่มทำงานเองทุกครั้งที่เปิดเครื่อง** ไม่ต้อง RDP เข้ามากด Start ใหม่ '
                  'ซึ่งสำคัญมากในหัวข้อที่ 12 เพราะเครื่องที่สร้างจาก AMI จะพร้อมให้บริการทันที'))
add(IMG(photo('19'), 'รูปที่ 11.19 ติดตั้ง Apache เป็น service และ Start'))
add(BOX('**ถ้าติ๊กช่อง Service ไม่ได้:** ต้องเปิด XAMPP Control Panel แบบ **Run as administrator** '
        '(คลิกขวาที่ไอคอน → Run as administrator) จึงจะติดตั้ง service ได้'))

add(SUB('ส่วน D: ตั้งค่า phpMyAdmin ให้เชื่อมต่อ RDS'))
add(STEP('11.20', 'เมื่อฐานข้อมูลมีสถานะ **Available** ไปที่ mysqlinstance → แท็บ **Connectivity & security** แล้วคัดลอก **Endpoint**'))
add(CODE(ENDPOINT))
add(P('Endpoint คือชื่อ DNS ของฐานข้อมูล ใช้แทน IP เวลาเชื่อมต่อ (Port **3306**)'))
add(IMG(photo('20'), 'รูปที่ 11.20 คัดลอก Endpoint ของฐานข้อมูล'))
add(STEP('11.21', 'ในเครื่อง EC2 เปิดไฟล์ **C:\\xampp\\phpMyAdmin\\config.inc.php** ด้วย Notepad แล้วหาบรรทัด host '
                  '(ใต้ /* Bind to the localhost ipv4 address and tcp */) เปลี่ยนจาก 127.0.0.1 เป็น Endpoint ของ RDS'))
add(CODE(f"$cfg['Servers'][$i]['host'] = '{ENDPOINT}';"))
add(IMG(photo('21', 1), 'รูปที่ 11.21 แก้ host ใน config.inc.php เป็น Endpoint ของ RDS'))
add(STEP('11.22', 'เปลี่ยน user จาก **root** เป็น Master username ของฐานข้อมูล (ดูได้ที่แท็บ Configuration ของ RDS)'))
add(CODE("$cfg['Servers'][$i]['user'] = 'mysqlAdmin';"))
add(IMG(photo('21', 0), 'รูปที่ 11.22 แก้ user เป็น mysqlAdmin'))
add(STEP('11.23', 'เปลี่ยน password จากค่าว่างเป็น Master password ที่ตั้งไว้ในขั้นตอนที่ 11.5 แล้ว**บันทึกไฟล์ (Ctrl + S)**'))
add(CODE("$cfg['Servers'][$i]['password'] = '<Master password ของ RDS>';"))
add(IMG(photo('22'), 'รูปที่ 11.23 ใส่ Master password ใน config.inc.php'))
add(BOX('**ข้อควรระวัง:** config.inc.php เก็บรหัสผ่านเป็นข้อความธรรมดา ใครเข้าเครื่องนี้ได้ก็อ่านรหัสผ่านฐานข้อมูลได้ '
        'และ auth_type = \'config\' ทำให้เปิด phpMyAdmin แล้ว**เข้าฐานข้อมูลได้ทันทีโดยไม่ต้องล็อกอิน**'))
add(STEP('11.24', 'ทดสอบเปิด **http://localhost/phpmyadmin** ในเครื่อง EC2 จะขึ้น Error **Cannot connect: invalid settings** และ '
                  '**mysqli::real_connect(): (HY000/2002): A connection attempt failed because the connected party did not properly respond '
                  'after a period of time** แปลว่าเชื่อมต่อไปที่ RDS แล้วหมดเวลา (timeout) เพราะ Security group ของ RDS ยังไม่อนุญาต EC2 เครื่องนี้'))
add(IMG(photo('23'), 'รูปที่ 11.24 phpMyAdmin เชื่อมต่อ RDS ไม่ได้'))

add(SUB('ส่วน E: แก้ Security group ของ RDS'))
add(STEP('11.25', 'กลับไปที่ mysqlinstance → แท็บ **Connectivity & security** → หัวข้อ Security คลิกลิงก์ **VPC security groups: '
                  'mySQLinstance (sg-0da62f55a8f532e78)**'))
add(IMG(photo('24'), 'รูปที่ 11.25 ลิงก์ VPC security group ของฐานข้อมูล'))
add(STEP('11.26', 'จะเปิดหน้า EC2 → **Security Groups** ที่กรองเฉพาะ mySQLinstance (Description: Created by RDS management console) '
                  'ติ๊กเลือกแล้วไปที่แท็บ **Inbound rules**'))
add(IMG(photo('25'), 'รูปที่ 11.26 Security group mySQLinstance'))
add(STEP('11.27', 'Inbound rule มีเพียง **MYSQL/Aurora TCP 3306** จาก Source **158.108.229.139/32** ซึ่งเป็น Public IP ของ'
                  '**คอมพิวเตอร์ที่ใช้สร้างฐานข้อมูล** (RDS console ใส่ให้อัตโนมัติ) ไม่ใช่ IP ของ EC2 (Private IP 172.31.20.89) '
                  'EC2 จึงเชื่อมต่อไม่ได้ ให้คลิก **Edit inbound rules**'))
add(IMG(photo('26'), 'รูปที่ 11.27 IP ที่ Security group อนุญาตไม่ตรงกับ IP ของ EC2'))
add(STEP('11.28', 'เปลี่ยน Source ของ rule MYSQL/Aurora เป็น **Anywhere-IPv4 (0.0.0.0/0)** แล้วคลิก **Save rules**'))
add(IMG(photo('27'), 'รูปที่ 11.28 เปลี่ยน Source เป็น 0.0.0.0/0'))
add(BOX('**ความปลอดภัย:** 0.0.0.0/0 ร่วมกับ Public access = Yes ทำให้ทุกคนบนอินเทอร์เน็ตพยายามเชื่อมต่อฐานข้อมูลได้ (กันไว้แค่รหัสผ่าน) '
        'วิธีที่ดีกว่าคือตั้ง Source เป็น **Custom → Security group MySGuseast2** (Security group ของ EC2) '
        'ซึ่งอนุญาตทุกเครื่องที่ใช้ MySGuseast2 รวมถึงเครื่องที่สองในหัวข้อที่ 12 โดยไม่ต้องรู้ IP และตั้ง Public access เป็น No'))
add(STEP('11.29', 'กลับไปที่ phpMyAdmin บน EC2 แล้วกด Refresh จะเข้า phpMyAdmin ได้ หัวข้อ Database server แสดง '
                  f'**Server: {ENDPOINT} via TCP/IP**, Server version **8.4.9** และ User **mysqlAdmin@172.31.20.89** '
                  '(เชื่อมต่อจาก Private IP ของ EC2) และด้านซ้ายมี database **myDB**'))
add(IMG(photo('28'), 'รูปที่ 11.29 phpMyAdmin เชื่อมต่อ RDS สำเร็จ'))
add(BOX('**Error สีแดงที่ยังเหลือ:** ข้อความ **Access denied for user \'pma\'** และ **Connection for controluser as defined in your '
        'configuration failed** เกิดจาก phpMyAdmin พยายามใช้ผู้ใช้ pma สำหรับฟีเจอร์เสริม ซึ่งไม่มีใน RDS **ไม่กระทบการใช้งาน** '
        'ถ้าต้องการซ่อน ให้ใส่ // หน้าบรรทัด controluser และ controlpass ใน config.inc.php'))

add(SUB('ส่วน F: ทดสอบสร้างตารางและเพิ่มข้อมูล'))
add(STEP('11.30', 'ใน phpMyAdmin คลิก **myDB** ด้านซ้าย → แท็บ **SQL** แล้วพิมพ์คำสั่งนี้ จากนั้นคลิก **Go**'))
add(CODE(['CREATE TABLE students(',
          '    student_id INT PRIMARY KEY,',
          '    name VARCHAR(100) NOT NULL',
          ');',
          "INSERT INTO students VALUES (6710450840, 'Sono G');"]))
add(IMG(photo('29'), 'รูปที่ 11.30 คำสั่ง SQL สร้างตาราง students'))
add(STEP('11.31', 'ผลลัพธ์จะขึ้น **MySQL returned an empty result set** (สร้างตารางสำเร็จ) และ **1 row inserted** '
                  'พร้อม Warning **#1264 Out of range value for column \'student_id\' at row 1** และตาราง students ปรากฏใต้ myDB'))
add(IMG(photo('30'), 'รูปที่ 11.31 สร้างตารางและเพิ่มข้อมูลสำเร็จ'))
add(BOX('**ทำไมขึ้น Warning #1264:** คอลัมน์ชนิด **INT** เก็บได้สูงสุด **2,147,483,647** แต่รหัสนิสิต 6710450840 มากกว่านั้น '
        'MySQL จึงเก็บเป็นค่าสูงสุด 2147483647 แทน (ดูขั้นตอนถัดไป) ถ้าต้องการเก็บรหัสนิสิตให้ถูกต้อง ให้ใช้ชนิด '
        '**BIGINT** หรือ **VARCHAR(10)** แทน INT'))
add(STEP('11.32', 'คลิกตาราง **students** (แท็บ Browse) จะเห็นข้อมูล 1 แถว คือ student_id **2147483647** และ name **Sono G**'))
add(IMG(photo('31'), 'รูปที่ 11.32 ข้อมูลในตาราง students'))

add(SUB('ส่วน G: สร้างหน้าเว็บ test.php ที่อ่านข้อมูลจาก RDS'))
add(STEP('11.33', 'ในเครื่อง EC2 สร้างไฟล์ **C:\\xampp\\htdocs\\test.php** (วิธีเดียวกับ Part 1 ขั้นตอนที่ 4.5 ต้องเป็น .php ไม่ใช่ .txt) '
                  'แล้วใส่โค้ดนี้ โดยแก้รหัสผ่านเป็น Master password ของเรา'))
add(CODE(['<?php',
          f"$pdo = new PDO('mysql:host={ENDPOINT};dbname=myDB', 'mysqlAdmin', '<Master password ของ RDS>');",
          '$stmt = $pdo->query("SELECT * FROM students");',
          '$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);',
          'foreach ($rows as $row) {',
          '    echo "ID: " . $row[\'student_id\'] . " - Name: " . $row[\'name\'] . "<br>";',
          '}',
          '?>']))
add(P('โค้ดนี้ใช้ **PDO** เชื่อมต่อ MySQL ที่ Endpoint ของ RDS (database myDB ด้วย mysqlAdmin) ดึงทุกแถวจากตาราง students '
      'แล้วแสดงทีละแถวในรูปแบบ ID: ... - Name: ...'))
add(IMG(photo('32'), 'รูปที่ 11.33 ไฟล์ test.php ใน htdocs'))
add(STEP('11.34', 'เปิด **http://localhost/test.php** ในเครื่อง EC2 จะแสดง **ID: 2147483647 - Name: Sono G** ซึ่งเป็นข้อมูลจาก RDS'))
add(IMG(photo('33'), 'รูปที่ 11.34 เปิด test.php บนเครื่อง EC2'))
add(BOX('**สังเกต:** ชื่อหน้าต่าง Remote Desktop ในรูปที่ 11.34 เปลี่ยนเป็น ec2-13-220-180-3 เพราะเครื่องถูก Stop/Start '
        '(เช่น session ของ AWS Academy หมดเวลา) Public IP จึงเปลี่ยนจาก 54.88.159.167 เป็น **13.220.180.3** '
        'แต่ Apache ยังทำงานอยู่เพราะติดตั้งเป็น service ไว้ (log: XAMPP Apache Service is already running on port 80)'))
add(STEP('11.35', 'ทดสอบจาก**คอมพิวเตอร์ของเราเอง** ด้วย **http://13.220.180.3/test.php** (ใช้ Public IP ปัจจุบันของ EC2) '
                  'จะเห็นผลลัพธ์เดียวกัน'))
add(IMG(photo('34'), 'รูปที่ 11.35 เปิด test.php จากคอมพิวเตอร์ของเรา'))

add(SUB('ส่วน H: เปิด phpMyAdmin จากภายนอก'))
add(STEP('11.36', 'ค่าเริ่มต้นของ XAMPP อนุญาตให้เปิด phpMyAdmin ได้เฉพาะจากในเครื่อง (localhost) ถ้าต้องการเปิดจากคอมพิวเตอร์ของเรา '
                  'ให้เปิดไฟล์ **C:\\xampp\\apache\\conf\\extra\\httpd-xampp.conf** (ค้นหาคำว่า httpd- ในโฟลเดอร์ C:\\xampp ได้) '
                  'เลื่อนลงล่างสุดที่ <Directory "C:/xampp/phpMyAdmin"> แล้วเปลี่ยน **Require local** เป็น **Require all granted**'))
add(CODE(['<Directory "C:/xampp/phpMyAdmin">',
          '    AllowOverride AuthConfig',
          '    Require all granted',
          '    ErrorDocument 403 /error/XAMPP_FORBIDDEN.html.var',
          '</Directory>']))
add(IMG(photo('35.1'), 'รูปที่ 11.36 แก้ httpd-xampp.conf ให้ phpMyAdmin เป็น Require all granted'))
add(STEP('11.37', 'บันทึกไฟล์ (ในแลปนี้แก้ส่วนของ webalizer เป็น Require all granted ด้วย ซึ่งไม่จำเป็น) '
                  'แล้ว**รีสตาร์ต Apache** (XAMPP Control Panel → Stop แล้ว Start ที่ Apache) เพื่อให้การตั้งค่าใหม่มีผล'))
add(IMG(photo('35.2'), 'รูปที่ 11.37 ส่วนท้ายของไฟล์ httpd-xampp.conf'))
add(STEP('11.38', 'จากคอมพิวเตอร์ของเรา เปิด **http://13.220.180.3/phpmyadmin/** จะเข้า phpMyAdmin ที่เชื่อมต่อ RDS ได้ '
                  '(User mysqlAdmin@172.31.20.89)'))
add(IMG(photo('36'), 'รูปที่ 11.38 เปิด phpMyAdmin จากคอมพิวเตอร์ของเรา'))
add(BOX('**อันตราย:** เมื่อเปิด Require all granted และใช้ auth_type = \'config\' **ทุกคนที่รู้ IP จะเข้าจัดการฐานข้อมูลได้ทันทีโดยไม่ต้องล็อกอิน** '
        'ใช้เฉพาะตอนทดสอบในแลป ในการใช้งานจริงให้คง Require local ไว้ หรือเปลี่ยน auth_type เป็น \'cookie\' เพื่อบังคับให้ล็อกอิน'))
add(BOX('**ยังไม่ต้องลบทรัพยากร:** หัวข้อที่ 12 ใช้ myWebAppServer และ mysqlinstance ต่อ วิธีลบทั้งหมดอยู่ท้ายหัวข้อที่ 12'))

# =====================================================================
# 12. ELB
# =====================================================================
add(H('12. Elastic Load Balancer (ELB)'))
add(SUB('วัตถุประสงค์'))
add(P('**Elastic Load Balancing (ELB)** คือบริการที่รับ request จากผู้ใช้แล้วกระจายไปยังเครื่องหลายเครื่อง (Target) '
      'ช่วยให้รองรับผู้ใช้ได้มากขึ้น และทำ **Health check** ตรวจสอบเครื่องเป็นระยะ ถ้าเครื่องใดเสีย Load Balancer จะหยุดส่งงานให้เครื่องนั้นโดยอัตโนมัติ '
      'ผู้ใช้เข้าเว็บผ่าน **DNS name** ของ Load Balancer ชื่อเดียว โดยไม่ต้องรู้ IP ของแต่ละเครื่อง'))
add(P('ในแลปนี้ใช้ **Application Load Balancer (ALB)** ซึ่งทำงานกับ HTTP/HTTPS โดยสร้างเครื่องที่สองจาก AMI ของ myWebAppServer '
      'ไว้คนละ Availability Zone ทั้งสองเครื่องใช้ฐานข้อมูล RDS ตัวเดียวกัน จึงแสดงข้อมูลเหมือนกันไม่ว่าผู้ใช้จะถูกส่งไปเครื่องไหน'))
add(TABLE(['ส่วนประกอบ', 'ชื่อ', 'ค่าที่ใช้'],
          [['AMI', 'myWebAppAMI', 'สร้างจาก myWebAppServer'],
           ['Web server 1', 'myWebAppServer', 'us-east-1c, Private IP 172.31.20.89'],
           ['Web server 2', 'myWebAppServer2', 'us-east-1a, Private IP 172.31.5.93 (สร้างจาก myWebAppAMI)'],
           ['Target group', 'myTG', 'Instances, HTTP:80, มีทั้ง 2 เครื่อง'],
           ['Load balancer', 'myLB', 'Application, Internet-facing, Listener HTTP:80 → myTG']],
          [2200, 2400, 4400]))

add(SUB('ส่วน A: สร้างเครื่องที่สองจาก AMI'))
add(STEP('12.1', 'ที่หน้า Instances ติ๊กเลือก **myWebAppServer** → **Actions** → **Image and templates** → **Create image**'))
add(IMG(photo('37'), 'รูปที่ 12.1 Create image จาก myWebAppServer'))
add(STEP('12.2', 'ตั้ง Image name = **myWebAppAMI** ไม่ต้องติ๊ก Reboot instance และใช้ volume เดิม (30 GiB gp3) แล้วคลิก **Create image**'))
add(IMG(photo('38'), 'รูปที่ 12.2 ตั้งค่า Create image'))
add(STEP('12.3', 'ไปที่ **Images** → **AMIs** จะเห็น myWebAppAMI (ami-0c9f8ff20264d0702) สถานะ **Pending** '
                 'ใช้เวลานานพอสมควร ระหว่างรอทำส่วน B ไปก่อนได้'))
add(IMG(photo('39'), 'รูปที่ 12.3 AMI สถานะ Pending'))
add(STEP('12.4', 'เมื่อสถานะเป็น **Available** ติ๊กเลือก myWebAppAMI แล้วคลิก **Launch instance from AMI**'))
add(IMG(photo('40'), 'รูปที่ 12.4 AMI พร้อมใช้งาน'))
add(STEP('12.5', 'ตั้งค่าเครื่องที่สองแล้วคลิก **Launch instance**'))
add(BUL('Name: **myWebAppServer2**'))
add(BUL('AMI: **myWebAppAMI** (เลือกไว้ให้แล้ว), Instance type: เปิด All generations → **m7i-flex.large**'))
add(BUL('Key pair: **MyKPuseast2**'))
add(BUL('VPC: **Default VPC**, Availability Zone: **us-east-1a** (**คนละ AZ กับเครื่องแรก** ที่อยู่ us-east-1c)'))
add(BUL('Auto-assign public IP: **Enable**, Firewall: **Select existing security group** → **MySGuseast2**, Storage: **30 GiB**'))
add(IMG(photo('41'), 'รูปที่ 12.5 สร้างเครื่องที่สองที่ us-east-1a'))
add(BOX('**ทำไมต้องคนละ AZ:** ถ้า AZ ใด AZ หนึ่งมีปัญหา (ไฟดับ เครือข่ายล่ม) เครื่องใน AZ อื่นยังให้บริการต่อได้ '
        'Load Balancer จะส่งผู้ใช้ไปเฉพาะเครื่องที่ยังทำงานอยู่'))
add(STEP('12.6', 'หน้า Instances จะมี 2 เครื่อง: **myWebAppServer2** (us-east-1a, Public IP 3.210.183.159, Private IP 172.31.5.93) '
                 'และ **myWebAppServer** (us-east-1c, Public IP 13.220.180.3)'))
add(IMG(photo('42'), 'รูปที่ 12.6 Web server ทั้ง 2 เครื่อง'))
add(STEP('12.7', 'เชื่อมต่อ RDP เข้า myWebAppServer2 ได้ด้วย**รหัสผ่านเดียวกับเครื่องแรก** เพราะ AMI คัดลอกบัญชีมาด้วย '
                 '(เหมือน Part 1 ขั้นตอนที่ 5.10) เครื่องนี้มี XAMPP, test.php และ config.inc.php ที่ตั้งค่าไว้ครบ'))
add(IMG(photo('43'), 'รูปที่ 12.7 เชื่อมต่อ RDP เข้า myWebAppServer2'))
add(STEP('12.8', 'จากคอมพิวเตอร์ของเรา เปิด **http://3.210.183.159/test.php** จะแสดง **ID: 2147483647 - Name: Sono G** ทันที '
                 'โดยไม่ต้องกด Start Apache เพราะ Apache เป็น service ที่เริ่มเองตอนเปิดเครื่อง'))
add(IMG(photo('44'), 'รูปที่ 12.8 เปิด test.php จากเครื่องที่สอง'))
add(STEP('12.9', 'เปิด **http://3.210.183.159/phpmyadmin/** จะเข้า phpMyAdmin ได้ โดย User เป็น **mysqlAdmin@172.31.5.93** '
                 '(Private IP ของเครื่องที่สอง) แสดงว่าทั้งสองเครื่องใช้ฐานข้อมูล RDS ตัวเดียวกัน'))
add(IMG(photo('45'), 'รูปที่ 12.9 เปิด phpMyAdmin จากเครื่องที่สอง'))

add(SUB('ส่วน B: สร้าง Application Load Balancer'))
add(STEP('12.10', 'ที่เมนูด้านซ้ายของ EC2 เลือก **Load Balancing** → **Load Balancers** (ตอนนี้ยังไม่มี) แล้วคลิก **Create load balancer**'))
add(IMG(photo('46'), 'รูปที่ 12.10 หน้า Load Balancers'))
add(STEP('12.11', 'เลือก **Application Load Balancer** แล้วคลิก **Create** '
                  '(Network Load Balancer ใช้กับ TCP/UDP ที่ต้องการความเร็วสูง ส่วน Gateway Load Balancer ใช้กับอุปกรณ์ด้านความปลอดภัย)'))
add(IMG(photo('47'), 'รูปที่ 12.11 เลือก Application Load Balancer'))
add(STEP('12.12', 'ตั้งค่า Basic configuration'))
add(BUL('Load balancer name: **myLB**'))
add(BUL('Scheme: **Internet-facing** (รับ request จากอินเทอร์เน็ต)'))
add(BUL('Load balancer IP address type: **IPv4**'))
add(BUL('VPC: **Default VPC (vpc-0ab1645036dc923b6)**'))
add(IMG(photo('48'), 'รูปที่ 12.12 ตั้งชื่อ myLB'))
add(STEP('12.13', 'ที่ **Availability Zones and subnets** ติ๊ก AZ ที่มีเครื่องอยู่ทั้งสองอัน'))
add(BUL('**us-east-1a** (use1-az1) → subnet-0a1e0ab754b787615 (myWebAppServer2)'))
add(BUL('**us-east-1c** (use1-az4) → subnet-0b84c8e05205251dd (myWebAppServer)'))
add(P('ที่ **Security groups** เลือก **MySGuseast2** (เปิด HTTP 80 ไว้แล้ว)'))
add(IMG(photo('49'), 'รูปที่ 12.13 เลือก AZ, Subnet และ Security group'))
add(BOX('**ข้อกำหนด:** Application Load Balancer ต้องเลือกอย่างน้อย **2 AZ** และต้องเลือก AZ ที่มีเครื่องอยู่ครบทุก AZ '
        'ถ้าไม่ได้เลือก AZ ของเครื่องใด Load Balancer จะส่ง request ไปเครื่องนั้นไม่ได้'))
add(STEP('12.14', 'ที่ **Listeners and routing** ใช้ Listener **HTTP : 80** และ Routing action **Forward to target groups** '
                  'แต่ช่อง Target group ยังไม่มีให้เลือก ให้คลิกลิงก์ **create target group** (จะเปิดแท็บใหม่ อย่าปิดแท็บเดิม)'))
add(IMG(photo('50'), 'รูปที่ 12.14 คลิก create target group'))
add(STEP('12.15', 'ตั้งค่า Target group แล้วคลิก **Next**'))
add(BUL('Target type: **Instances**'))
add(BUL('Target group name: **myTG**'))
add(BUL('Protocol : Port: **HTTP : 80**, IP address type: **IPv4**'))
add(BUL('VPC: **Default VPC**, Protocol version: **HTTP1**'))
add(IMG(photo('51'), 'รูปที่ 12.15 ตั้งค่า Target group myTG'))
add(STEP('12.16', 'Health checks ใช้ค่าเริ่มต้นไปก่อน (Protocol **HTTP**, Path **/**) จะแก้ในส่วน C แล้วคลิก **Next**'))
add(IMG(photo('52'), 'รูปที่ 12.16 Health checks ค่าเริ่มต้น'))
add(STEP('12.17', 'ที่ **Register targets** ติ๊กเลือก**ทั้งสองเครื่อง** (myWebAppServer2 และ myWebAppServer) ใส่ Ports = **80** '
                  'คลิก **Include as pending below** จะเห็น Targets (2) อยู่ในรายการ Pending แล้วคลิก **Next**'))
add(IMG(photo('53'), 'รูปที่ 12.17 เพิ่มทั้งสองเครื่องเป็น Target'))
add(STEP('12.18', 'ตรวจสอบหน้า Review แล้วคลิก **Create target group**'))
add(IMG(photo('54'), 'รูปที่ 12.18 Review target group'))
add(STEP('12.19', 'จะขึ้น **Successfully created the target group: myTG** มี 2 Targets สถานะ **Unused** '
                  'เพราะยังไม่ได้ผูกกับ Load Balancer (Load balancer: None associated)'))
add(IMG(photo('55'), 'รูปที่ 12.19 Target group myTG ที่สร้างเสร็จ'))
add(STEP('12.20', 'กลับไปที่แท็บสร้าง Load Balancer เดิม คลิกปุ่ม **Refresh** (ลูกศรวงกลม) ข้างช่อง Target group แล้วเลือก **myTG**'))
add(IMG(photo('56'), 'รูปที่ 12.20 เลือก Target group myTG'))
add(STEP('12.21', 'เลื่อนลงไปที่ **Summary** ตรวจสอบ (myLB, Internet-facing, 2 AZ, MySGuseast2, HTTP:80 → 1 target group) '
                  'แล้วคลิก **Create load balancer** สถานะจะเป็น Provisioning ประมาณ 2–5 นาทีก่อนเป็น **Active**'))
add(IMG(photo('57'), 'รูปที่ 12.21 ตรวจสอบแล้ว Create load balancer'))

add(SUB('ส่วน C: ปรับ Health check'))
add(STEP('12.22', 'ไปที่ **Target Groups** → **myTG** → แท็บ **Health checks** จะเห็นว่าทั้ง 2 Targets ยังเป็น **Initial** '
                  'ค่าเริ่มต้นคือ Healthy threshold 5 ครั้ง, Unhealthy threshold 2 ครั้ง, Timeout 5 วินาที, Interval 30 วินาที, '
                  'Success codes 200 ให้คลิก **Edit**'))
add(IMG(photo('58'), 'รูปที่ 12.22 Health check settings ของ myTG'))
add(STEP('12.23', 'เปิด **Advanced health check settings** แล้วแก้ค่าดังตาราง จากนั้นคลิก **Save changes**'))
add(TABLE(['ค่า', 'ก่อนแก้', 'หลังแก้', 'เหตุผล'],
          [['Healthy threshold', '5', '2', 'ผ่าน 2 ครั้งติดก็ถือว่าเครื่องพร้อม'],
           ['Unhealthy threshold', '2', '2', 'ไม่เปลี่ยน'],
           ['Timeout', '5 วินาที', '14 วินาที', 'Windows/Apache ตอบช้าได้ (ต้องน้อยกว่า Interval)'],
           ['Interval', '30 วินาที', '15 วินาที', 'ตรวจถี่ขึ้น'],
           ['Success codes', '200', '200-499', 'หน้า / ของ XAMPP ตอบเป็น redirect ไม่ใช่ 200']],
          [2200, 1500, 1500, 3800]))
add(IMG(photo('59'), 'รูปที่ 12.23 ค่า Health check ก่อนแก้'))
add(IMG(photo('60'), 'รูปที่ 12.24 ค่า Health check หลังแก้'))
add(BOX('**ทำไมต้องแก้:** Health check path คือ / ซึ่ง XAMPP จะ redirect ไปที่ /dashboard/ (ตอบรหัส 3xx) ถ้า Success codes เป็น 200 อย่างเดียว '
        'Load Balancer จะมองว่าเครื่อง **Unhealthy** และไม่ส่งผู้ใช้ไปให้ การใส่ 200-499 จึงทำให้ผ่าน '
        'และค่าใหม่ทำให้เครื่องเป็น Healthy ภายในประมาณ 30 วินาที (2 × 15) แทน 150 วินาที (5 × 30)'))

add(SUB('ส่วน D: ทดสอบ Load Balancer'))
add(STEP('12.24', 'ไปที่ **Load Balancers** → **myLB** ตรวจสอบว่า Status เป็น **Active** แล้วคัดลอก **DNS name**'))
add(CODE(LB_DNS))
add(IMG(photo('61'), 'รูปที่ 12.25 รายละเอียดของ myLB และ DNS name'))
add(STEP('12.25', f'จากคอมพิวเตอร์ของเรา เปิด **http://{LB_DNS.lower()}/test.php** จะแสดง **ID: 2147483647 - Name: Sono G** '
                  'แสดงว่า Load Balancer ส่ง request ไปยัง Web server และ Web server อ่านข้อมูลจาก RDS ได้'))
add(IMG(photo('62'), 'รูปที่ 12.26 เปิด test.php ผ่าน Load Balancer'))
add(STEP('12.26', f'เปิด **http://{LB_DNS.lower()}/phpmyadmin/** จะเข้า phpMyAdmin ได้ โดย User เป็น **mysqlAdmin@172.31.5.93** '
                  'แปลว่าครั้งนี้ Load Balancer ส่งไปที่ **myWebAppServer2** ถ้ากด Refresh หลายครั้ง IP อาจสลับเป็น 172.31.20.89 (myWebAppServer)'))
add(IMG(photo('63'), 'รูปที่ 12.27 เปิด phpMyAdmin ผ่าน Load Balancer'))
add(STEP('12.27', 'ทดสอบว่า Load Balancer ทำงานถูกต้องเมื่อเครื่องเสีย (โน้ตในรูปที่ 12.28):', keep_next=True))
add(BUL('Stop เครื่องใดเครื่องหนึ่ง (เช่น myWebAppServer) แล้วรอให้ Target นั้นเป็น Unhealthy ในแท็บ Targets ของ myTG'))
add(BUL('เปิด test.php และ phpMyAdmin ด้วย IP ของเครื่องที่ Stop → **เปิดไม่ได้**'))
add(BUL('เปิดด้วย IP ของอีกเครื่อง และด้วย **DNS name ของ Load Balancer** → **ยังเปิดได้** เพราะ Load Balancer ส่งไปเฉพาะเครื่องที่ Healthy'))
add(BUL('ทำซ้ำโดยสลับเป็น Stop อีกเครื่อง แล้ว Start เครื่องทั้งสองกลับ'))
add(IMG(photo('67'), 'รูปที่ 12.28 โน้ตวิธีทดสอบ Load Balancer'))
add(BOX('**หมายเหตุ:** เมื่อ Start เครื่องกลับมา Public IP จะเปลี่ยน แต่ DNS name ของ Load Balancer ไม่เปลี่ยน '
        'นี่คือเหตุผลที่ผู้ใช้ควรเข้าเว็บผ่าน Load Balancer ไม่ใช่ IP ของเครื่อง'))

add(SUB('ส่วน E: คืนทรัพยากร (Clean up)'))
add(STEP('12.28', 'เมื่อทำ Part 4 เสร็จ ให้ลบทรัพยากรตามลำดับนี้เพื่อไม่ให้เสีย credit ของ AWS Academy', keep_next=False))
add(BUL('Load Balancers → myLB → Actions → **Delete load balancer**'))
add(BUL('Target Groups → myTG → Actions → **Delete**'))
add(BUL('Instances → **Terminate** myWebAppServer และ myWebAppServer2'))
add(BUL('AMIs → myWebAppAMI → Actions → **Deregister AMI** แล้วไปลบ Snapshot ของ AMI ที่ Elastic Block Store → Snapshots'))
add(BUL('Aurora and RDS → Databases → mysqlinstance → Actions → **Delete** (ไม่ต้องสร้าง final snapshot และไม่ต้องเก็บ automated backups)'))
add(BUL('Security Groups → ลบ mySQLinstance (ทำได้หลังลบฐานข้อมูลแล้ว)'))

# ---------- Summary ----------
add(H('สรุป Part 4'))
add(SUB('ค่าที่ใช้ในแลปนี้ (ใช้อ้างอิงเมื่อทำซ้ำ)'))
add(TABLE(['รายการ', 'ค่าที่ใช้', 'หมายเหตุ'],
          [['RDS DB instance', 'mysqlinstance', 'MySQL Community 8.4.9, db.t3.micro, Single-AZ, us-east-1c'],
           ['RDS storage', 'gp3 100 GiB', 'AWS Academy สร้างเกิน 100 GB ไม่ได้'],
           ['Endpoint : Port', f'{ENDPOINT} : 3306', 'ใช้ใน config.inc.php และ test.php'],
           ['Database / ผู้ใช้', 'myDB / mysqlAdmin', 'Public access Yes'],
           ['SG ของ RDS', 'mySQLinstance (sg-0da62f55a8f532e78)', 'MYSQL/Aurora 3306 จาก 0.0.0.0/0'],
           ['ตาราง', 'students(student_id INT, name VARCHAR(100))', 'INT เก็บรหัสนิสิต 10 หลักไม่ได้'],
           ['Web server 1', 'myWebAppServer (i-074f2a7d199174feb)', 'us-east-1c, 172.31.20.89, Public 13.220.180.3'],
           ['AMI', 'myWebAppAMI (ami-0c9f8ff20264d0702)', 'สร้างจาก Web server 1'],
           ['Web server 2', 'myWebAppServer2 (i-0d9ac77b8604246e4)', 'us-east-1a, 172.31.5.93, Public 3.210.183.159'],
           ['Target group', 'myTG', 'HTTP:80, Healthy 2, Timeout 14 s, Interval 15 s, Success 200-499'],
           ['Load balancer', 'myLB (Application, Internet-facing)', f'{LB_DNS}, HTTP:80 → myTG'],
           ['ไฟล์ที่แก้บน EC2', 'config.inc.php, httpd-xampp.conf, htdocs\\test.php', 'host/user/password, Require all granted']],
          [2200, 3600, 3200]))
add(SUB('สิ่งที่ควรจำจาก Part 4'))
add(BUL('RDS คือฐานข้อมูลแบบ Managed ที่ AWS ดูแลเครื่อง การติดตั้ง และการสำรองข้อมูลให้ เราเชื่อมต่อผ่าน Endpoint และ Port 3306'))
add(BUL('ตั้ง Initial database name ตอนสร้าง ไม่อย่างนั้นจะไม่มี database ให้ใช้ และใน AWS Academy ต้องใช้ storage ไม่เกิน 100 GB'))
add(BUL('Security group ที่ RDS สร้างให้อนุญาตเฉพาะ IP ของคอมพิวเตอร์ที่ใช้สร้าง ต้องแก้ให้ EC2 เข้าได้ (ดีที่สุดคืออ้างอิง Security group ของ EC2)'))
add(BUL('phpMyAdmin เชื่อมต่อ RDS ได้โดยแก้ host, user และ password ใน config.inc.php และต้องระวังเรื่องรหัสผ่านที่เก็บเป็นข้อความธรรมดา'))
add(BUL('ติดตั้ง Apache เป็น service ทำให้เครื่องที่ Start ใหม่หรือสร้างจาก AMI ให้บริการได้ทันที'))
add(BUL('Web server ที่ไม่เก็บข้อมูลไว้ในเครื่อง (ใช้ RDS ร่วมกัน) สามารถสร้างเพิ่มจาก AMI และวางหลัง Load Balancer ได้'))
add(BUL('Application Load Balancer ต้องใช้อย่างน้อย 2 AZ ส่งงานผ่าน Target group และส่งไปเฉพาะเครื่องที่ผ่าน Health check'))
add(BUL('ถ้า Health check path ตอบเป็น redirect ต้องตั้ง Success codes ให้ครอบคลุม (เช่น 200-499) ไม่อย่างนั้นเครื่องจะเป็น Unhealthy'))
add(PAGEBREAK())

splice_part(UN, 4, ''.join(X), IMG)
