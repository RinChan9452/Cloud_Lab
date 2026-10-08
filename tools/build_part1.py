"""Part 1 content (Thai). Usage: python build_part1.py <unpacked_docx_dir> "D:/Cloud lab/Part 1" """
import sys
from report_lib import H, SUB, P, STEP, BUL, BOX, CODE, TABLE, PAGEBREAK, Images, load_photos, splice_part

UN, PHOTOS = sys.argv[1], sys.argv[2]
photos = load_photos(PHOTOS)
def photo(key, idx=0):
    return photos[key][idx]
IMG = Images(UN, 'part1', docpr_base=1000)

X = []
add = X.append

# ---------- Intro ----------
add(P('Part 1 เป็นการเรียนรู้บริการเครื่องเสมือน (Virtual Machine) ของ AWS คือ **Amazon EC2 (Elastic Compute Cloud)** '
      'โดยจะสร้างเครื่อง Windows Server บนคลาวด์ ติดตั้ง Web server และ Database ด้วยตัวเอง (Self-managed) '
      'จากนั้นสร้าง AMI เพื่อนำไปสร้างเครื่องที่สองที่เหมือนเครื่องแรกทุกประการ'))
add(P('การทำงานแบ่งเป็น 5 หัวข้อ ซึ่งต้องทำตามลำดับ เพราะหัวข้อหลังต้องใช้สิ่งที่สร้างในหัวข้อก่อน'))
add(BUL('**Key pair** – ใช้ถอดรหัสรหัสผ่าน Administrator ของเครื่อง Windows (ใช้ในหัวข้อที่ 3)'))
add(BUL('**Security Group** – ไฟร์วอลล์ที่กำหนดว่าพอร์ตใดเข้าเครื่องได้ (ใช้ในหัวข้อที่ 3)'))
add(BUL('**EC2 Instance** – เครื่องเสมือน Windows Server ที่เชื่อมต่อผ่าน Remote Desktop'))
add(BUL('**Self-managed DB web server** – ติดตั้ง XAMPP (Apache + MySQL + PHP) บนเครื่อง'))
add(BUL('**AMI** – สร้าง image ของเครื่องที่ตั้งค่าเสร็จแล้ว และสร้างเครื่องใหม่จาก image นั้น'))
add(BOX('**ก่อนเริ่ม:** ทุกขั้นตอนในแลปนี้ทำใน Region **United States (N. Virginia) us-east-1** '
        'ให้ตรวจสอบที่มุมขวาบนของ AWS Console ทุกครั้ง เพราะ Key pair, Security Group และ AMI ผูกอยู่กับ Region '
        'ถ้าเลือก Region ผิดจะมองไม่เห็น resource ที่สร้างไว้'))

# ---------- 1. Key pair ----------
add(H("1. Create a key pair for encrypt&decrypt EC2 instance's authentication password."))
add(SUB('วัตถุประสงค์'))
add(P('Key pair คือคู่กุญแจแบบ Asymmetric cryptography ประกอบด้วย **Public key** (AWS เก็บไว้และใส่ลงในเครื่อง EC2) '
      'และ **Private key** (ไฟล์ .pem ที่เราดาวน์โหลดเก็บไว้) สำหรับเครื่อง Windows นั้น AWS จะสุ่มรหัสผ่านของบัญชี '
      'Administrator แล้วเข้ารหัสด้วย Public key ดังนั้นเฉพาะผู้ที่มี Private key เท่านั้นจึงจะถอดรหัสและเห็นรหัสผ่านได้'))
add(P('หลักการ: Asymmetric cryptography (public key และ private key) ใช้แจกจ่าย secret key ที่ใช้ใน Symmetric cryptography '
      'อย่างปลอดภัย จากนั้น HTTP request รวมถึงรหัสผ่านของ Windows server จะถูกเข้ารหัสด้วย secret key นั้น'))
add(SUB('ขั้นตอนการทำ'))
add(STEP('1.1', 'เข้าสู่ AWS Management Console พิมพ์ **EC2** ในช่อง Search ด้านบน แล้วเลือกบริการ EC2 จะเข้าสู่หน้า '
                '**EC2 Dashboard** ตรวจสอบว่ามุมขวาบนเป็น Region **United States (N. Virginia)**'))
add(IMG(photo('1'), 'รูปที่ 1.1 หน้า EC2 Dashboard'))
add(STEP('1.2', 'ที่เมนูด้านซ้าย เลือก **Network & Security > Key Pairs** จะเห็นรายการ Key pair ที่มีอยู่'))
add(IMG(photo('2'), 'รูปที่ 1.2 หน้ารายการ Key pairs'))
add(STEP('1.3', 'คลิกปุ่ม **Create key pair** (ปุ่มสีส้ม มุมขวาบน) จะเข้าสู่หน้ากรอกข้อมูล'))
add(IMG(photo('3'), 'รูปที่ 1.3 หน้า Create key pair'))
add(STEP('1.4', 'กรอกข้อมูลดังนี้ แล้วคลิก **Create key pair**'))
add(BUL('Name: **MyKPuseast2** (ตั้งชื่อให้บอก Region จะได้จำง่าย)'))
add(BUL('Key pair type: **RSA** (ต้องเป็น RSA เพราะ Windows instance ไม่รองรับ ED25519 สำหรับการถอดรหัสรหัสผ่าน)'))
add(BUL('Private key file format: **.pem** (ใช้ถอดรหัสรหัสผ่าน Windows บน AWS Console และใช้กับ OpenSSH ได้)'))
add(IMG(photo('4'), 'รูปที่ 1.4 กรอกข้อมูล Key pair'))
add(BOX('**หมายเหตุ:** ถ้าขึ้นข้อความ **The keypair already exists** (ดังในรูปที่ 1.4) แปลว่ามี Key pair ชื่อนี้อยู่แล้ว '
        'เช่น กดปุ่มสร้างซ้ำหลังจากสร้างสำเร็จไปแล้ว ให้กลับไปตรวจสอบในรายการ หรือเปลี่ยนเป็นชื่ออื่น'))
add(STEP('1.5', 'เมื่อสร้างสำเร็จ เบราว์เซอร์จะดาวน์โหลดไฟล์ **MyKPuseast2.pem** ลงโฟลเดอร์ Downloads อัตโนมัติ '
                'และ Key pair ใหม่จะแสดงในรายการ'))
add(IMG(photo('4.2'), 'รูปที่ 1.5 Key pair MyKPuseast2 ที่สร้างเสร็จแล้ว'))
add(BOX('**สำคัญ:** ไฟล์ .pem ดาวน์โหลดได้ครั้งเดียวเท่านั้น ถ้าทำหายจะถอดรหัสรหัสผ่าน Windows ของเครื่องที่ใช้ '
        'Key pair นี้ไม่ได้ ให้เก็บไว้ในที่ปลอดภัย ห้ามแชร์ให้ผู้อื่น และห้าม commit ขึ้น Git'))

# ---------- 2. Security group ----------
add(H('2. Create a Security Group.'))
add(SUB('วัตถุประสงค์'))
add(P('Security Group (SG) ทำหน้าที่เป็น **ไฟร์วอลล์เสมือน (Virtual firewall) ระดับ instance** กำหนดว่าทราฟฟิกขาเข้า '
      '(Inbound) และขาออก (Outbound) ที่พอร์ตใดและมาจากที่ใดจึงจะผ่านได้ ค่าเริ่มต้นคือปฏิเสธขาเข้าทั้งหมดและอนุญาตขาออกทั้งหมด '
      'SG เป็นแบบ **Stateful** คือถ้าอนุญาต request ขาเข้าแล้ว response ขากลับจะผ่านได้อัตโนมัติ'))
add(P('ในแลปนี้ต้องเปิด 3 พอร์ต คือ HTTP (80) และ HTTPS (443) สำหรับเข้าเว็บ และ RDP (3389) สำหรับ Remote Desktop '
      'เข้าไปจัดการเครื่อง Windows'))
add(SUB('ขั้นตอนการทำ'))
add(STEP('2.1', 'ที่เมนูด้านซ้าย เลือก **Network & Security > Security Groups** จะเห็นรายการ Security Group ที่มีอยู่ '
                '(เช่น default ของ VPC)'))
add(IMG(photo('5'), 'รูปที่ 2.1 หน้ารายการ Security Groups'))
add(STEP('2.2', 'คลิก **Create security group** จะเข้าสู่หน้ากรอกข้อมูล ซึ่งตอนแรกยังไม่มี Inbound rule'))
add(IMG(photo('6'), 'รูปที่ 2.2 หน้า Create security group (ยังไม่มี Inbound rules)'))
add(STEP('2.3', 'กรอก **Basic details**'))
add(BUL('Security group name: **MySGuseast2** (แก้ชื่อภายหลังไม่ได้)'))
add(BUL('Description: **SGuseast2**'))
add(BUL('VPC: ใช้ Default VPC (vpc-0ab1645036dc923b6)'))
add(STEP('2.4', 'ในส่วน **Inbound rules** คลิก **Add rule** 3 ครั้ง แล้วตั้งค่าตามตาราง '
                '(Protocol และ Port range จะเติมให้อัตโนมัติเมื่อเลือก Type)'))
add(TABLE(['Type', 'Protocol', 'Port', 'Source', 'ใช้ทำอะไร'],
          [['HTTP', 'TCP', '80', 'Anywhere-IPv4 (0.0.0.0/0)', 'เปิดเว็บผ่าน http://'],
           ['HTTPS', 'TCP', '443', 'Anywhere-IPv4 (0.0.0.0/0)', 'เปิดเว็บผ่าน https://'],
           ['RDP', 'TCP', '3389', 'Anywhere-IPv4 (0.0.0.0/0)', 'Remote Desktop เข้าเครื่อง Windows']],
          [1300, 1100, 900, 2600, 3100]))
add(STEP('2.5', 'ส่วน **Outbound rules** ใช้ค่าเริ่มต้น (All traffic ไปยัง 0.0.0.0/0) เพื่อให้เครื่องออกอินเทอร์เน็ตได้ '
                '(เช่น ดาวน์โหลด XAMPP) จากนั้นเลื่อนลงล่างสุดแล้วคลิก **Create security group**'))
add(IMG(photo('7'), 'รูปที่ 2.3 ตั้งค่า Basic details, Inbound rules และ Outbound rules'))
add(STEP('2.6', 'ตรวจสอบผล: **MySGuseast2** แสดงในรายการ โดย Inbound rules count = **3 Permission entries** '
                'และ Outbound rules count = 1 Permission entry'))
add(IMG(photo('8'), 'รูปที่ 2.4 Security group MySGuseast2 ที่สร้างเสร็จแล้ว'))
add(BOX('**ข้อควรระวัง:** Source 0.0.0.0/0 หมายถึงทุก IP บนอินเทอร์เน็ต AWS จึงแสดงคำเตือนสีเหลือง '
        'ใช้ได้สำหรับแลป แต่ในระบบจริงควรตั้ง Source ของ RDP เป็น **My IP** เพื่อไม่ให้คนอื่นพยายามล็อกอินเข้าเครื่อง'))

# ---------- 3. EC2 ----------
add(H('3. Provision an EC2 Instance.'))
add(SUB('วัตถุประสงค์'))
add(P('สร้างเครื่องเสมือน (EC2 Instance) ระบบปฏิบัติการ **Windows Server 2025** โดยใช้ Key pair และ Security Group '
      'จากหัวข้อที่ 1 และ 2 จากนั้นเชื่อมต่อเข้าเครื่องด้วย **Remote Desktop Protocol (RDP)**'))
add(SUB('ส่วน A: สร้าง Instance'))
add(STEP('3.1', 'ที่เมนูด้านซ้าย เลือก **Instances > Instances** แล้วคลิก **Launch instances** '
                '(ตอนนี้ยังไม่มี instance ใน Region นี้)'))
add(IMG(photo('9'), 'รูปที่ 3.1 หน้า Instances ก่อนสร้างเครื่อง'))
add(STEP('3.2', 'จะเข้าสู่หน้า **Launch an instance** ซึ่งค่าเริ่มต้นเป็น Amazon Linux และ t3.micro '
                'ต้องเปลี่ยนค่าตามขั้นตอนถัดไป'))
add(IMG(photo('10'), 'รูปที่ 3.2 หน้า Launch an instance (ค่าเริ่มต้น)'))
add(STEP('3.3', 'ตั้งค่าส่วนบนของหน้า'))
add(BUL('Name and tags: ใส่ชื่อเครื่อง เช่น **MyWebDBserver** (หรือตั้งภายหลังก็ได้ ดูขั้นตอนที่ 3.7)'))
add(BUL('Application and OS Images (AMI): แท็บ **Quick Start** เลือก **Windows** → '
        '**Microsoft Windows Server 2025 Base** (Free tier eligible, 64-bit x86)'))
add(BUL('Instance type: เปิดสวิตช์ **All generations** แล้วเลือก **m7i-flex.large** (2 vCPU, 8 GiB Memory) '
        'เพราะ t3.micro มีหน่วยความจำเพียง 1 GiB ไม่พอสำหรับ Windows Server ที่ต้องรัน XAMPP'))
add(IMG(photo('11', 0), 'รูปที่ 3.3 เลือก AMI Windows Server 2025 และ Instance type m7i-flex.large'))
add(STEP('3.4', 'เลื่อนลงมาตั้งค่าส่วนล่าง แล้วคลิก **Launch instance** ที่แถบ Summary ด้านขวา'))
add(BUL('Key pair (login): เลือก **MyKPuseast2** (จากหัวข้อที่ 1)'))
add(BUL('Network settings: Network = Default VPC, Subnet = No preference, Auto-assign public IP = **Enable** '
        '(เพื่อให้เครื่องมี Public IP และเข้าถึงจากภายนอกได้)'))
add(BUL('Firewall (security groups): เลือก **Select existing security group** → **MySGuseast2** (จากหัวข้อที่ 2)'))
add(BUL('Configure storage: **30 GiB gp3** (ค่าเริ่มต้นของ Windows และอยู่ในโควตา Free tier 30 GB)'))
add(IMG(photo('11', 1), 'รูปที่ 3.4 ตั้งค่า Key pair, Network settings และ Storage'))
add(STEP('3.5', 'กลับมาที่หน้า Instances จะเห็นเครื่องใหม่มี Instance state = **Running** แต่ Status check ยังเป็น '
                '**Initializing** ให้รอประมาณ 3–5 นาที โดยกดปุ่ม Refresh เป็นระยะ'))
add(IMG(photo('12'), 'รูปที่ 3.5 Instance กำลัง Initializing'))
add(STEP('3.6', 'เมื่อ Status check เปลี่ยนเป็น **3/3 checks passed** แสดงว่าเครื่องพร้อมใช้งาน ให้จดค่า '
                '**Public IPv4 address** ไว้ (ในแลปนี้คือ 100.31.253.78) เพื่อใช้ทดสอบเว็บในหัวข้อที่ 4'))
add(IMG(photo('13'), 'รูปที่ 3.6 Instance พร้อมใช้งาน (3/3 checks passed)'))
add(SUB('ส่วน B: เชื่อมต่อเครื่องด้วย Remote Desktop (RDP)'))
add(STEP('3.7', 'ถ้ายังไม่ได้ตั้งชื่อ ให้คลิกไอคอนดินสอในคอลัมน์ Name แล้วตั้งชื่อเป็น **MyWebDBserver** '
                'จากนั้นติ๊กเลือก instance แล้วคลิกปุ่ม **Connect** ด้านบน (แท็บ Details ด้านล่างจะแสดง Public และ Private IP ของเครื่อง)'))
add(IMG(photo('14'), 'รูปที่ 3.7 ตั้งชื่อ Instance และคลิก Connect'))
add(STEP('3.8', 'หน้า **Connect to Windows instance** จะเปิดแท็บ In web browser (SSM Session Manager) เป็นค่าเริ่มต้น '
                'ซึ่งใช้ไม่ได้ในแลปนี้เพราะเครื่องไม่มี IAM role (จะขึ้น Not connected) ให้เปลี่ยนไปที่แท็บ '
                '**RDP (Remote Desktop Protocol)**'))
add(IMG(photo('15'), 'รูปที่ 3.8 แท็บ In web browser ใช้ไม่ได้ ให้เปลี่ยนไปแท็บ RDP'))
add(STEP('3.9', 'ในแท็บ RDP จะเห็นข้อมูลที่ต้องใช้ ได้แก่ Public DNS, Username = **Administrator** และลิงก์ '
                'Get Windows password ให้คลิก **Download** ใต้หัวข้อ RDP shortcut file เพื่อดาวน์โหลดไฟล์ .rdp'))
add(IMG(photo('16'), 'รูปที่ 3.9 แท็บ RDP และปุ่ม Download RDP shortcut file'))
add(STEP('3.10', 'เปิดไฟล์ .rdp ที่ดาวน์โหลดมา (โปรแกรม Remote Desktop Connection ของ Windows จะเปิดขึ้น) '
                 'จะมีคำเตือน Unknown publisher เพราะไฟล์ไม่ได้ลงลายเซ็นดิจิทัล ให้คลิก **Connect**'))
add(IMG(photo('17'), 'รูปที่ 3.10 คำเตือนเมื่อเปิดไฟล์ RDP shortcut'))
add(STEP('3.11', 'หน้าต่าง Windows Security จะถามรหัสผ่านของ Administrator ซึ่งเรายังไม่มี '
                 'ให้เปิดหน้าต่างนี้ค้างไว้ แล้วกลับไปขอรหัสผ่านที่ AWS Console'))
add(IMG(photo('18'), 'รูปที่ 3.11 หน้าต่างขอรหัสผ่าน Administrator'))
add(STEP('3.12', 'ที่แท็บ RDP บน AWS Console คลิก **Get Windows password** จะเข้าสู่หน้าที่แสดง Instance ID '
                 'และ Key pair ที่ผูกกับเครื่อง (MyKPuseast2)'))
add(IMG(photo('19'), 'รูปที่ 3.12 หน้า Get Windows password'))
add(STEP('3.13', 'คลิก **Upload private key file** แล้วเลือกไฟล์ **MyKPuseast2.pem** จากโฟลเดอร์ Downloads '
                 '(เนื้อหาไฟล์จะถูกใส่ในช่อง Private key contents) จากนั้นคลิก **Decrypt password**'))
add(IMG(photo('20'), 'รูปที่ 3.13 อัปโหลดไฟล์ .pem เพื่อถอดรหัสรหัสผ่าน'))
add(STEP('3.14', 'AWS จะแสดง Username และ **Password** ที่ถอดรหัสแล้ว ให้คลิกไอคอนคัดลอกหน้า Password'))
add(IMG(photo('21'), 'รูปที่ 3.14 รหัสผ่าน Administrator ที่ถอดรหัสแล้ว'))
add(BOX('**หมายเหตุ:** ถ้าเพิ่งสร้างเครื่อง อาจต้องรอประมาณ 4 นาทีหลัง launch รหัสผ่านจึงจะพร้อมให้ถอดรหัส'))
add(STEP('3.15', 'กลับไปที่หน้าต่าง Windows Security วางรหัสผ่านแล้วคลิก **OK** จะมีคำเตือน '
                 'The identity of the remote computer cannot be verified (เพราะเครื่องใช้ certificate ที่สร้างเอง) ให้คลิก **Yes**'))
add(IMG(photo('22'), 'รูปที่ 3.15 คำเตือนเรื่อง Certificate ให้คลิก Yes'))
add(STEP('3.16', 'หน้าต่าง Remote Desktop จะแสดง Desktop ของ Windows Server บน EC2 แสดงว่าเชื่อมต่อสำเร็จ '
                 'ทุกอย่างที่ทำในหน้าต่างนี้คือการทำงานบนเครื่องในคลาวด์'))
add(IMG(photo('23'), 'รูปที่ 3.16 เชื่อมต่อ Remote Desktop เข้า Windows Server สำเร็จ'))

# ---------- 4. Self-managed DB web server ----------
add(H('4. Create a Self-managed DB web server.'))
add(SUB('วัตถุประสงค์'))
add(P('ติดตั้ง Web server และ Database server บนเครื่อง EC2 ด้วยตัวเอง (Self-managed) โดยใช้ **XAMPP** '
      'ซึ่งเป็นชุดโปรแกรมที่รวม Apache (Web server), MySQL/MariaDB (Database), PHP และ Perl ไว้ด้วยกัน '
      'คำว่า Self-managed หมายถึงเราต้องดูแลเองทั้งหมด ทั้งการติดตั้ง อัปเดต สำรองข้อมูล และแก้ปัญหา '
      '(ต่างจาก Managed service เช่น Amazon RDS ใน Part 4 ที่ AWS ดูแลให้)'))
add(BOX('ขั้นตอนในหัวข้อนี้ทำ**ภายในหน้าต่าง Remote Desktop ของเครื่อง MyWebDBserver** ทั้งหมด '
        'ยกเว้นขั้นตอนที่ 4.6 ที่ทดสอบจากคอมพิวเตอร์ของเราเอง'))
add(SUB('ขั้นตอนการทำ'))
add(STEP('4.1', 'ปิด Windows Firewall ของเครื่อง: เปิด Start → **Windows Security** → **Firewall & network protection** '
                '→ คลิก **Public network (active)** → สลับ **Microsoft Defender Firewall** เป็น **Off** '
                '(ทำแบบเดียวกันกับ Private network) เหตุผลคือ Windows Firewall จะบล็อกการเชื่อมต่อขาเข้าที่พอร์ต 80 '
                'ทำให้เข้าเว็บจากภายนอกไม่ได้ แม้ Security Group จะเปิดพอร์ตไว้แล้วก็ตาม'))
add(IMG(photo('24'), 'รูปที่ 4.1 ปิด Microsoft Defender Firewall ของ Public network'))
add(STEP('4.2', 'เปิด Microsoft Edge ในเครื่อง EC2 ไปที่ **https://www.apachefriends.org** หัวข้อ '
                '**XAMPP for Windows** แล้วคลิก **Download (64 bit)** (เลือกเวอร์ชันใดก็ได้ เช่น 8.2.12 / PHP 8.2.12)'))
add(IMG(photo('25'), 'รูปที่ 4.2 หน้าดาวน์โหลด XAMPP for Windows'))
add(STEP('4.3', 'เปิดไฟล์ติดตั้ง XAMPP ในหน้า **Select Components** ให้เลือกเฉพาะที่จำเป็น คือ '
                '**Apache, MySQL, PHP และ phpMyAdmin** แล้วเอาเครื่องหมายออกจากตัวอื่น (FileZilla FTP Server, '
                'Mercury Mail Server, Tomcat, Perl, Webalizer, Fake Sendmail) เพื่อให้ติดตั้งเร็วและใช้ทรัพยากรน้อย '
                'จากนั้นกด Next จนจบ โดยใช้โฟลเดอร์ติดตั้งเริ่มต้น **C:\\xampp** '
                '(ด้านหลังจะเห็นว่า Firewall ของ Private และ Public network ปิดแล้ว)'))
add(IMG(photo('26'), 'รูปที่ 4.3 เลือก Components ที่จะติดตั้งใน XAMPP'))
add(STEP('4.4', 'เปิด **XAMPP Control Panel** แล้วคลิก **Start** ที่แถว **Apache** และ **MySQL** '
                'เมื่อสำเร็จชื่อโมดูลจะเป็นสีเขียว แสดงพอร์ตที่ใช้ (Apache: 80, 443 / MySQL: 3306) '
                'และ log แสดง Status change detected: running'))
add(IMG(photo('27'), 'รูปที่ 4.4 Start Apache และ MySQL ใน XAMPP Control Panel'))
add(STEP('4.5', 'สร้างหน้าเว็บทดสอบ: เปิดโฟลเดอร์ **C:\\xampp\\htdocs** (กดปุ่ม Explorer ใน XAMPP Control Panel '
                'แล้วเข้าโฟลเดอร์ htdocs) ซึ่งเป็น Document root ของ Apache คลิกขวา → New → Text Document '
                'ตั้งชื่อ HelloWorld แล้วเปิดด้วย Notepad และพิมพ์โค้ดนี้'))
add(CODE("<?php echo 'Hello World!';?>"))
add(P('บันทึกไฟล์ แล้วเปลี่ยนนามสกุลจาก **.txt** เป็น **.php** (ต้องเปิด View → Show → File name extensions '
      'ใน File Explorer ก่อนจึงจะเห็นนามสกุล) จะได้ไฟล์ **helloworld.php**'))
add(IMG(photo('28'), 'รูปที่ 4.5 สร้างไฟล์ HelloWorld ใน C:\\xampp\\htdocs'))
add(STEP('4.6', 'ทดสอบจาก**คอมพิวเตอร์ของเราเอง** (นอก Remote Desktop): เปิดเบราว์เซอร์แล้วเข้า '
                '**http://<Public IPv4>/helloworld.php** ในแลปนี้คือ http://100.31.253.78/helloworld.php '
                'ถ้าหน้าเว็บแสดง **Hello World!** แสดงว่า Apache และ PHP ทำงานถูกต้อง และเข้าถึงได้จากอินเทอร์เน็ตผ่าน '
                'Security Group พอร์ต 80'))
add(IMG(photo('29'), 'รูปที่ 4.6 เปิด helloworld.php จากเบราว์เซอร์บนเครื่องของเราได้สำเร็จ'))
add(BOX('**ถ้าเปิดเว็บไม่ได้ ให้ตรวจสอบตามลำดับนี้**'))
add(BUL('ใช้ **http://** ไม่ใช่ https:// (ยังไม่ได้ติดตั้ง SSL certificate)'))
add(BUL('Apache ใน XAMPP Control Panel ยังเป็นสีเขียว (Running)'))
add(BUL('Security Group มี Inbound rule HTTP พอร์ต 80'))
add(BUL('Windows Firewall ของเครื่องปิดอยู่'))
add(BUL('ชื่อไฟล์ถูกต้อง เป็น helloworld.php ไม่ใช่ helloworld.php.txt'))
add(BUL('ใช้ Public IP ปัจจุบัน เพราะ Public IP จะเปลี่ยนทุกครั้งที่ Stop/Start เครื่อง '
        '(ถ้าต้องการ IP คงที่ให้ใช้ Elastic IP ใน Part 2)'))

# ---------- 5. AMI ----------
add(H('5. Create and launch AMI (Amazon Machine Image).'))
add(SUB('วัตถุประสงค์'))
add(P('**AMI (Amazon Machine Image)** คือแม่แบบ (template) ของเครื่อง ที่เก็บระบบปฏิบัติการ โปรแกรมที่ติดตั้ง '
      'และการตั้งค่าทั้งหมดของเครื่องต้นฉบับ ในหัวข้อนี้จะสร้าง AMI จากเครื่อง MyWebDBserver ที่ติดตั้ง XAMPP เสร็จแล้ว '
      'จากนั้นนำ AMI ไปสร้างเครื่องที่สอง ซึ่งจะมีทุกอย่างเหมือนเครื่องแรก (Firewall ที่ปิดไว้, XAMPP และไฟล์ helloworld.php) '
      'โดยไม่ต้องติดตั้งใหม่'))
add(SUB('ส่วน A: สร้าง AMI'))
add(STEP('5.1', 'ที่หน้า Instances ติ๊กเลือก **MyWebDBserver** → คลิก **Actions** → **Image and templates** → **Create image**'))
add(IMG(photo('30'), 'รูปที่ 5.1 เมนู Actions > Image and templates > Create image'))
add(STEP('5.2', 'กรอก Image name เป็น **myAMIwebDBserver** (แก้ไขภายหลังไม่ได้) ส่วน Image description ไม่บังคับ '
                'Instance volumes ใช้ค่าเดิม (EBS 30 GiB) แล้วคลิก **Create image**'))
add(IMG(photo('31'), 'รูปที่ 5.2 หน้า Create image'))
add(BOX('**ตัวเลือก Reboot instance:** ถ้าติ๊ก AWS จะ reboot เครื่องก่อนทำ snapshot ทำให้ข้อมูลบนดิสก์สมบูรณ์ '
        '(data consistency) ในแลปนี้ไม่ได้ติ๊ก หากในเครื่องมีฐานข้อมูลที่ใช้งานจริง แนะนำให้ติ๊ก หรือ Stop MySQL ก่อนสร้าง AMI'))
add(STEP('5.3', 'ไปที่เมนู **Images > AMIs** จะเห็น myAMIwebDBserver มีสถานะ **Pending** ใช้เวลาประมาณ 5–10 นาทีหรือนานกว่า '
                '(เพราะต้องทำ snapshot ของดิสก์ 30 GiB) ระหว่างรอสามารถทำงานอื่นไปก่อนได้'))
add(IMG(photo('32'), 'รูปที่ 5.3 AMI อยู่ในสถานะ Pending'))
add(STEP('5.4', 'เมื่อสถานะเปลี่ยนเป็น **Available** จึงจะนำ AMI ไปใช้ได้'))
add(IMG(photo('33'), 'รูปที่ 5.4 AMI อยู่ในสถานะ Available'))
add(SUB('ส่วน B: สร้างเครื่องที่สองจาก AMI'))
add(STEP('5.5', 'ติ๊กเลือก AMI myAMIwebDBserver แล้วคลิก **Launch instance from AMI** จะเข้าสู่หน้า Launch an instance '
                'ที่เลือก AMI ของเราไว้แล้ว (สังเกตว่า Instance type กลับเป็น t3.micro และ Key pair ยังว่าง ต้องตั้งค่าใหม่)'))
add(IMG(photo('34'), 'รูปที่ 5.5 หน้า Launch an instance จาก AMI'))
add(STEP('5.6', 'ตั้งค่าส่วนบนให้เหมือนเครื่องแรก'))
add(BUL('Name: **MyWebDBserver2**'))
add(BUL('AMI: แท็บ **My AMIs** → Owned by me → **myAMIwebDBserver**'))
add(BUL('Instance type: เปิด All generations → **m7i-flex.large**'))
add(IMG(photo('35'), 'รูปที่ 5.6 เลือก My AMIs และ Instance type'))
add(STEP('5.7', 'ตั้งค่าส่วนล่าง แล้วคลิก **Launch instance**'))
add(BUL('Key pair: **MyKPuseast2**'))
add(BUL('Firewall: Select existing security group → **MySGuseast2**'))
add(BUL('Storage: **30 GiB gp3**'))
add(IMG(photo('36'), 'รูปที่ 5.7 ตั้งค่า Key pair, Security group และ Storage'))
add(STEP('5.8', 'กลับมาที่หน้า Instances จะเห็น 2 เครื่อง (เปลี่ยนชื่อเครื่องแรกเป็น **MyWebDBserver1** เพื่อแยกง่าย) '
                'เครื่องใหม่ MyWebDBserver2 ได้ Public IP ใหม่ (3.81.65.121) ให้รอจน Status check เป็น 3/3 checks passed'))
add(IMG(photo('37'), 'รูปที่ 5.8 เครื่องที่สองกำลัง Initializing'))
add(STEP('5.9', 'ติ๊กเลือก **MyWebDBserver2** แล้วคลิก **Connect**'))
add(IMG(photo('38'), 'รูปที่ 5.9 เลือกเครื่องที่สองแล้วคลิก Connect'))
add(STEP('5.10', 'ที่แท็บ **RDP** คลิก Download RDP shortcut file → เปิดไฟล์ → คลิก **Connect** '
                 'แล้วล็อกอินด้วย Username Administrator และ**รหัสผ่านเดียวกับเครื่องแรก** '
                 'เพราะ AMI คัดลอกบัญชีผู้ใช้และรหัสผ่านมาด้วย (ไม่ต้อง Get Windows password ใหม่)'))
add(IMG(photo('39'), 'รูปที่ 5.10 เชื่อมต่อ RDP เข้าเครื่องที่สอง'))
add(STEP('5.11', 'เมื่อเข้าเครื่องที่สองได้ จะเห็นว่าเหมือนเครื่องแรก (ซ้ายคือเครื่องที่ 1 ขวาคือเครื่องที่ 2) '
                 'Windows Firewall ปิดอยู่แล้วและมี XAMPP ติดตั้งอยู่ ถ้ามีหน้าต่าง **Shutdown Event Tracker** '
                 'ถามสาเหตุการปิดเครื่อง (เพราะ AMI ถูกสร้างขณะเครื่องกำลังทำงาน) ให้เลือกเหตุผลใดก็ได้หรือกด Cancel'))
add(IMG(photo('40'), 'รูปที่ 5.11 เครื่องที่ 1 (ซ้าย) และเครื่องที่ 2 (ขวา) ที่สร้างจาก AMI'))
add(STEP('5.12', 'เปิด XAMPP Control Panel บนเครื่องที่สอง กด **Start** ที่ Apache แล้วทดสอบจากเครื่องของเราด้วย '
                 'http://3.81.65.121/helloworld.php จะแสดง **Hello World!** เหมือนเครื่องแรก '
                 '(ไม่ได้สร้างไฟล์ใหม่ ไฟล์ถูกคัดลอกมาจาก AMI) ตอนนี้จึงมี Web server 2 เครื่องที่ให้บริการเนื้อหาเดียวกัน'))
add(IMG(photo('41'), 'รูปที่ 5.12 ทั้งสองเครื่องแสดง Hello World! ได้'))
add(BOX('**หมายเหตุเรื่อง MySQL:** ในรูปที่ 5.12 จะเห็น error **MySQL shutdown unexpectedly** ซึ่งพบบ่อยกับ MySQL ของ XAMPP '
        'เมื่อเครื่องถูกปิดหรือถูกทำ image ขณะ MySQL ทำงานอยู่ การทดสอบ helloworld.php ใช้เพียง Apache และ PHP '
        'จึงไม่ได้รับผลกระทบ ถ้าต้องการใช้ MySQL วิธีแก้ที่ใช้กันทั่วไปคือ ปิด XAMPP → เปลี่ยนชื่อโฟลเดอร์ '
        'C:\\xampp\\mysql\\data เป็น data_old → คัดลอกโฟลเดอร์ C:\\xampp\\mysql\\backup มาตั้งชื่อเป็น data → '
        'คัดลอกโฟลเดอร์ฐานข้อมูลของเราและไฟล์ ibdata1 จาก data_old มาใส่ใน data → Start MySQL ใหม่'))

# ---------- Summary ----------
add(H('สรุป Part 1'))
add(SUB('ค่าที่ใช้ในแลปนี้ (ใช้อ้างอิงเมื่อทำซ้ำ)'))
add(TABLE(['รายการ', 'ค่าที่ใช้', 'หมายเหตุ'],
          [['Region', 'us-east-1 (N. Virginia)', 'ทุก resource ต้องอยู่ Region เดียวกัน'],
           ['Key pair', 'MyKPuseast2 (RSA, .pem)', 'ใช้ถอดรหัสรหัสผ่าน Windows'],
           ['Security Group', 'MySGuseast2', 'Inbound: HTTP 80, HTTPS 443, RDP 3389'],
           ['AMI ต้นทาง', 'Microsoft Windows Server 2025 Base', 'Quick Start > Windows'],
           ['Instance type', 'm7i-flex.large (2 vCPU, 8 GiB)', 'ต้องเปิด All generations ก่อนจึงจะเห็น'],
           ['Storage', '30 GiB gp3', 'ค่าเริ่มต้นของ Windows'],
           ['เครื่องที่ 1', 'MyWebDBserver1 (100.31.253.78)', 'สร้างจาก Windows AMI'],
           ['AMI ที่สร้าง', 'myAMIwebDBserver', 'สร้างจากเครื่องที่ 1'],
           ['เครื่องที่ 2', 'MyWebDBserver2 (3.81.65.121)', 'สร้างจาก myAMIwebDBserver'],
           ['Web root', 'C:\\xampp\\htdocs', 'ไฟล์ทดสอบ helloworld.php']],
          [2000, 3500, 3500]))
add(SUB('สิ่งที่ควรจำจาก Part 1'))
add(BUL('ลำดับการสร้างคือ Key pair → Security Group → EC2 → ติดตั้งซอฟต์แวร์ → AMI '
        'ต้องสร้าง Key pair และ Security Group ก่อน เพราะต้องเลือกตอน Launch instance'))
add(BUL('เก็บไฟล์ .pem ให้ดี เพราะดาวน์โหลดได้ครั้งเดียว'))
add(BUL('Security Group คือไฟร์วอลล์ระดับ AWS ส่วน Windows Firewall คือไฟร์วอลล์ระดับ OS '
        'ทราฟฟิกต้องผ่านทั้งสองชั้นจึงจะเข้าถึงเว็บได้'))
add(BUL('Public IP เปลี่ยนเมื่อ Stop/Start เครื่อง ถ้าต้องการ IP คงที่ให้ใช้ Elastic IP (Part 2)'))
add(BUL('เครื่องที่สร้างจาก AMI จะได้ทุกอย่างเหมือนต้นฉบับ รวมถึงโปรแกรม ไฟล์ และรหัสผ่าน Administrator'))
add(BUL('หลังทำแลปเสร็จ ให้ Stop หรือ Terminate instance และลบ AMI/Snapshot ที่ไม่ใช้ เพื่อไม่ให้เสีย credit ของ AWS Academy'))
add(PAGEBREAK())

splice_part(UN, 1, ''.join(X), IMG)
