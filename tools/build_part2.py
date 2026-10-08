"""Part 2 content (Thai). Usage: python build_part2.py <unpacked_docx_dir> "D:/Cloud lab/Part 2" """
import sys
from report_lib import H, SUB, P, STEP, BUL, BOX, CODE, TABLE, PAGEBREAK, Images, load_photos, splice_part

UN, PHOTOS = sys.argv[1], sys.argv[2]
photos = load_photos(PHOTOS)
def photo(key, idx=0):
    return photos[key][idx]
IMG = Images(UN, 'part2', docpr_base=2000)

X = []
add = X.append

# ---------- Intro ----------
add(P('Part 2 เป็นการเรียนรู้บริการเครือข่ายเสมือนของ AWS ประกอบด้วย 2 แลปและการบ้าน 1 ชิ้น'))
add(BUL('**Elastic IP** – ทดลองให้เห็นว่า Public IP ปกติของ EC2 จะเปลี่ยนทุกครั้งที่ Stop/Start เครื่อง '
        'และใช้ Elastic IP เพื่อให้เครื่องมี Public IP คงที่'))
add(BUL('**Manually created VPC** – สร้างเครือข่ายส่วนตัว (VPC) เองทีละส่วน ได้แก่ VPC, Subnet, Internet Gateway และ '
        'Route Table แล้วสร้าง EC2 ในเครือข่ายนั้น และทดสอบว่าเข้าถึงได้จากอินเทอร์เน็ต'))
add(BUL('**Homework** – สร้าง VPC ที่มี 2 Subnet อยู่คนละ Availability Zone วาง EC2 Subnet ละ 2 เครื่อง ผูก Elastic IP '
        'ให้ทุกเครื่อง แล้วทดสอบ ping จากคอมพิวเตอร์ของเราและ ping ระหว่างเครื่องด้วยกัน'))
add(BOX('**ก่อนเริ่ม:** ทุกขั้นตอนทำใน Region **United States (N. Virginia) us-east-1** เหมือน Part 1 '
        'และใช้ Key pair **MyKPuseast2** กับ Security Group **MySGuseast2** ที่สร้างไว้ใน Part 1'))

# ---------- 6. Elastic IP ----------
add(H('6. Elastic IP'))
add(SUB('วัตถุประสงค์'))
add(P('เมื่อสร้าง EC2 ใน Subnet ที่เปิด Auto-assign public IP ไว้ AWS จะสุ่ม Public IP จากกลุ่ม IP ของ AWS มาให้ '
      'แต่ IP นี้**ไม่ใช่ของเราถาวร** เมื่อ Stop เครื่อง AWS จะคืน IP นั้นกลับไป และเมื่อ Start ใหม่จะได้ IP ใหม่ '
      'ทำให้ผู้ใช้ที่จำ IP เดิมไว้เข้าเว็บไม่ได้'))
add(P('**Elastic IP (EIP)** คือ Public IPv4 แบบคงที่ที่จองไว้ในบัญชี AWS ของเรา (Allocate) และนำไปผูกกับ instance (Associate) ได้ '
      'IP จะไม่เปลี่ยนแม้ Stop/Start เครื่อง และย้ายไปผูกกับเครื่องอื่นได้ทันทีถ้าเครื่องเดิมเสีย'))
add(SUB('ส่วน A: สร้างเครื่องทดสอบและดูว่า Public IP เปลี่ยน'))
add(STEP('6.1', 'ไปที่ EC2 → **Instances** → **Launch instances** แล้วตั้งค่าส่วนบน'))
add(BUL('Name: เว้นว่างได้ (เครื่องนี้ใช้ทดสอบ IP เท่านั้น)'))
add(BUL('AMI: แท็บ Quick Start → **Amazon Linux** → **Amazon Linux 2023 kernel-6.18 AMI** (Free tier eligible) '
        'ใช้ Linux เพราะ boot เร็วกว่า Windows ทำให้ทดสอบ Stop/Start ได้เร็ว'))
add(BUL('Instance type: เปิด **All generations** → **m7i-flex.large**'))
add(IMG(photo('1', 0), 'รูปที่ 6.1 เลือก Amazon Linux 2023 และ Instance type'))
add(STEP('6.2', 'ตั้งค่าส่วนล่าง'))
add(BUL('Key pair: **ไม่ต้องเลือก** (ปล่อยเป็น Select)'))
add(BUL('Network settings: ใช้ค่าเริ่มต้น คือ Default VPC, Subnet = No preference, Auto-assign public IP = **Enable**'))
add(BUL('Firewall: **Select existing security group** → **MySGuseast2**'))
add(BUL('Storage: **8 GiB gp3** (ค่าเริ่มต้นของ Amazon Linux)'))
add(IMG(photo('1', 1), 'รูปที่ 6.2 ตั้งค่า Key pair, Network settings และ Storage'))
add(STEP('6.3', 'คลิก **Launch instance** จะมีหน้าต่างเตือนว่ายังไม่ได้เลือก Key pair ให้เลือก **Proceed without key pair** '
                'แล้วคลิก **Launch instance** อีกครั้ง'))
add(IMG(photo('2'), 'รูปที่ 6.3 เลือก Proceed without key pair'))
add(BOX('**ทำไมไม่ใช้ Key pair:** เครื่องนี้ใช้ดูการเปลี่ยนแปลงของ Public IP บนหน้า AWS Console เท่านั้น ไม่ต้องล็อกอินเข้าเครื่อง '
        'แต่ถ้าสร้างเครื่องที่ต้องใช้งานจริง ต้องเลือก Key pair เสมอ เพราะถ้าไม่มีจะล็อกอินเข้าเครื่องไม่ได้'))
add(STEP('6.4', 'รอจน Status check เป็น **3/3 checks passed** แล้วคลิกที่ instance เพื่อดูแท็บ Details '
                'จด **Public IPv4 address** ไว้ (ในแลปนี้คือ **34.229.50.79** ซึ่งแสดงเป็น Auto-assigned IP address)'))
add(IMG(photo('3'), 'รูปที่ 6.4 Public IP ก่อน Stop เครื่อง (34.229.50.79)'))
add(STEP('6.5', 'ติ๊กเลือก instance → **Instance state** → **Stop instance** รอจนสถานะเป็น Stopped '
                'จากนั้น **Instance state** → **Start instance** แล้วดู Public IPv4 address อีกครั้ง '
                'จะเห็นว่าเปลี่ยนเป็น **3.81.69.91** (ไม่ใช่ IP เดิม)'))
add(IMG(photo('4'), 'รูปที่ 6.5 หลัง Stop/Start Public IP เปลี่ยนเป็น 3.81.69.91'))
add(SUB('ส่วน B: จองและผูก Elastic IP'))
add(STEP('6.6', 'ที่เมนูด้านซ้ายของ EC2 เลือก **Network & Security** → **Elastic IPs** จะเห็นรายการ Elastic IP ที่จองไว้ '
                'แล้วคลิก **Allocate Elastic IP address**'))
add(IMG(photo('5'), 'รูปที่ 6.6 หน้า Elastic IP addresses'))
add(STEP('6.7', 'ตั้งค่า Public IPv4 address pool = **Amazon\'s pool of IPv4 addresses** และ Network border group = '
                '**us-east-1** (ค่าเริ่มต้นทั้งคู่) แล้วคลิก **Allocate**'))
add(IMG(photo('6'), 'รูปที่ 6.7 หน้า Allocate Elastic IP address'))
add(STEP('6.8', 'จะขึ้นข้อความ **Elastic IP address allocated successfully** และ IP ใหม่แสดงในรายการ '
                'โดยคอลัมน์ Associated instance ID ยังว่าง (ยังไม่ได้ผูกกับเครื่องใด)'))
add(IMG(photo('7'), 'รูปที่ 6.8 จอง Elastic IP สำเร็จ'))
add(STEP('6.9', 'ติ๊กเลือก Elastic IP → **Actions** → **Associate Elastic IP address** '
                '(หรือคลิกปุ่ม Associate this Elastic IP address บนแถบสีเขียว)'))
add(IMG(photo('8'), 'รูปที่ 6.9 เมนู Actions > Associate Elastic IP address'))
add(STEP('6.10', 'ตั้งค่าแล้วคลิก **Associate**'))
add(BUL('Resource type: **Instance**'))
add(BUL('Instance: เลือก instance ที่สร้างในขั้นตอนที่ 6.1 (**i-06d8ea70aba72516f**)'))
add(BUL('Private IP address: เว้นว่าง (AWS จะผูกกับ Private IP หลักของเครื่องให้)'))
add(BUL('Reassociation: ไม่ต้องติ๊ก'))
add(IMG(photo('9'), 'รูปที่ 6.10 เลือก Instance ที่จะผูก Elastic IP'))
add(BOX('**หมายเหตุ:** รูปที่ 6.8 และ 6.9 เป็น IP 32.194.18.1 แต่รูปที่ 6.10 เป็น 44.196.101.93 เพราะในแลปนี้กด Allocate ไปหลายครั้ง '
        'IP ที่ใช้จริงคือ **44.196.101.93** ไม่ว่าจะได้ IP ใดก็ทำขั้นตอนเหมือนกัน'))
add(STEP('6.11', 'จะขึ้นข้อความ **Elastic IP address associated successfully** และคอลัมน์ Associated instance ID '
                 'แสดง instance ของเรา (Private IP 172.31.34.186)'))
add(IMG(photo('10'), 'รูปที่ 6.11 ผูก Elastic IP 44.196.101.93 กับ instance สำเร็จ'))
add(SUB('ส่วน C: ทดสอบว่า IP ไม่เปลี่ยน'))
add(STEP('6.12', 'กลับไปที่หน้า Instances จะเห็นว่า **Public IPv4 address** และ **Elastic IP** ของเครื่องเป็น **44.196.101.93** '
                 'และ Auto-assigned IP address เปลี่ยนเป็น "–" (เครื่องใช้ Elastic IP แทน IP ที่สุ่มมา)'))
add(IMG(photo('11'), 'รูปที่ 6.12 Instance ใช้ Elastic IP 44.196.101.93'))
add(STEP('6.13', 'ทดสอบ **Stop instance** ระหว่างที่สถานะเป็น Stopping Public IPv4 ยังเป็น 44.196.101.93'))
add(IMG(photo('12'), 'รูปที่ 6.13 Stop instance แล้ว IP ยังเป็น Elastic IP'))
add(STEP('6.14', '**Start instance** อีกครั้ง Public IPv4 ยังเป็น **44.196.101.93** เหมือนเดิม '
                 'แสดงว่า Elastic IP ทำให้เครื่องมี IP คงที่จริง'))
add(IMG(photo('13'), 'รูปที่ 6.14 หลัง Start ใหม่ IP ยังเป็น 44.196.101.93'))
add(SUB('ส่วน D: คืน Elastic IP (Clean up)'))
add(STEP('6.15', 'ที่หน้า Instances ติ๊กเลือก instance → **Actions** → **Networking** → **Disassociate Elastic IP address** '
                 'แล้วยืนยัน (ต้อง Disassociate ก่อนจึงจะ Release ได้)'))
add(IMG(photo('14'), 'รูปที่ 6.15 Disassociate Elastic IP address'))
add(STEP('6.16', 'กลับไปที่ **Elastic IPs** ติ๊กเลือก Elastic IP ที่ไม่ใช้แล้ว → **Actions** → **Release Elastic IP addresses** → '
                 'ยืนยัน **Release** ทำซ้ำจนครบทุก IP ที่จองไว้ (ในแลปนี้มี 4 IP ได้แก่ 23.21.244.24, 32.194.18.1, '
                 '34.195.209.207 และ 44.196.101.93)'))
add(IMG(photo('15'), 'รูปที่ 6.16 Release Elastic IP addresses'))
add(BOX('**สำคัญ:** AWS คิดเงินค่า Public IPv4 address ทุก IP รวมถึง Elastic IP ที่จองไว้แต่ไม่ได้ผูกกับเครื่องใด '
        'หลังทำแลปเสร็จให้ Release ทุก IP ที่ไม่ใช้ และ Terminate เครื่องทดสอบ เพื่อไม่ให้เสีย credit ของ AWS Academy'))

# ---------- 7. Manually created VPC ----------
add(H('7. Manually created VPC'))
add(SUB('วัตถุประสงค์'))
add(P('**VPC (Virtual Private Cloud)** คือเครือข่ายส่วนตัวที่แยกออกจากลูกค้าคนอื่นบน AWS ทุกบัญชีจะมี **Default VPC** '
      '(172.31.0.0/16) ที่ตั้งค่าให้พร้อมใช้ ซึ่งเครื่องใน Part 1 และหัวข้อที่ 6 ใช้อยู่ ในหัวข้อนี้จะสร้าง VPC ใหม่เอง '
      'ทีละส่วนเพื่อให้เข้าใจว่าแต่ละส่วนทำหน้าที่อะไร'))
add(TABLE(['ส่วนประกอบ', 'หน้าที่', 'ค่าที่ใช้ในแลปนี้'],
          [['VPC', 'กำหนดช่วง IP ทั้งหมดของเครือข่าย', 'myVPC – 10.0.0.0/16 (65,536 IP)'],
           ['Subnet', 'แบ่งช่วง IP ย่อยของ VPC ไว้ใน Availability Zone หนึ่ง', 'mySubnet – 10.0.1.0/24 (256 IP) ที่ us-east-1a'],
           ['Internet Gateway (IGW)', 'ประตูเชื่อม VPC กับอินเทอร์เน็ต', 'myIGW'],
           ['Route Table', 'บอกว่าทราฟฟิกไปปลายทางใดต้องส่งไปทางไหน', 'myRT – 0.0.0.0/0 → myIGW'],
           ['Security Group', 'ไฟร์วอลล์ของ instance (ผูกกับ VPC)', 'mySG2myVPC – RDP, ICMP']],
          [2200, 3600, 3200]))
add(BOX('**หลักการ:** Subnet จะเป็น **Public subnet** (เข้าถึงจากอินเทอร์เน็ตได้) ก็ต่อเมื่อ Route Table ของ Subnet นั้นมีเส้นทาง '
        '**0.0.0.0/0 → Internet Gateway** และเครื่องใน Subnet มี Public IP ถ้าขาดอย่างใดอย่างหนึ่งจะเข้าเครื่องจากภายนอกไม่ได้'))
add(SUB('ส่วน A: สร้าง VPC'))
add(STEP('7.1', 'พิมพ์ **VPC** ในช่อง Search แล้วเลือกบริการ VPC จะเข้าสู่หน้า **VPC dashboard** '
                'ซึ่งแสดงจำนวน resource ใน Region (ตอนนี้มีเฉพาะของ Default VPC: VPC 1, Subnet 6, Route table 1, '
                'Internet gateway 1) แล้วคลิก **Create VPC**'))
add(IMG(photo('16'), 'รูปที่ 7.1 หน้า VPC dashboard'))
add(STEP('7.2', 'หน้า Create VPC จะเลือก **VPC and more** ไว้เป็นค่าเริ่มต้น ซึ่งจะสร้าง VPC พร้อม Subnet, Route table '
                'และ Gateway ให้อัตโนมัติ (ดูได้จาก Preview ด้านขวา) แต่แลปนี้ต้องการสร้างเองทีละส่วน จึงต้องเปลี่ยนเป็น **VPC only**'))
add(IMG(photo('17'), 'รูปที่ 7.2 ค่าเริ่มต้น VPC and more'))
add(STEP('7.3', 'ตั้งค่าดังนี้ แล้วคลิก **Create VPC**'))
add(BUL('Resources to create: **VPC only**'))
add(BUL('Name tag: **myVPC**'))
add(BUL('IPv4 CIDR block: **IPv4 CIDR manual input** → IPv4 CIDR = **10.0.0.0/16**'))
add(BUL('IPv6 CIDR block: **No IPv6 CIDR block**'))
add(BUL('Tenancy: **Default** (ถ้าเลือก Dedicated จะเสียเงินเพิ่มมาก)'))
add(BUL('VPC encryption control: **None**'))
add(IMG(photo('18'), 'รูปที่ 7.3 ตั้งค่า VPC only และ IPv4 CIDR 10.0.0.0/16'))
add(STEP('7.4', 'จะขึ้นข้อความ **You successfully created vpc-0d2baa5b377dfd013** และ myVPC แสดงในรายการ '
                'สถานะ Available, IPv4 CIDR 10.0.0.0/16 (อีกแถวคือ Default VPC 172.31.0.0/16)'))
add(IMG(photo('19'), 'รูปที่ 7.4 myVPC ที่สร้างเสร็จแล้ว'))
add(SUB('ส่วน B: สร้าง Subnet'))
add(STEP('7.5', 'ที่เมนูด้านซ้าย เลือก **Subnets** จะเห็น Subnet 6 อันของ Default VPC (172.31.x.x/20) '
                'แล้วคลิก **Create subnet**'))
add(IMG(photo('20'), 'รูปที่ 7.5 หน้า Subnets'))
add(STEP('7.6', 'ตั้งค่าดังนี้ แล้วคลิก **Create subnet**'))
add(BUL('VPC ID: **vpc-0d2baa5b377dfd013 (myVPC)**'))
add(BUL('Subnet name: **mySubnet**'))
add(BUL('Availability Zone: **United States (N. Virginia) / use1-az1 (us-east-1a)**'))
add(BUL('IPv4 VPC CIDR block: **10.0.0.0/16**'))
add(BUL('IPv4 subnet CIDR block: **10.0.1.0/24** (256 IP และต้องอยู่ในช่วงของ VPC)'))
add(IMG(photo('21', 0), 'รูปที่ 7.6 ตั้งค่า Subnet'))
add(STEP('7.7', 'mySubnet แสดงในรายการ (subnet-096ebe4b829069873) โดย Available IPv4 addresses = **251** '
                'เพราะ AWS สงวน 5 IP แรกและ IP สุดท้ายของทุก Subnet ไว้ใช้เอง (256 − 5 = 251) '
                'สังเกตว่า Auto-assign public IPv4 address = **No** จึงต้องเปิดเองตอนสร้าง instance'))
add(IMG(photo('21', 1), 'รูปที่ 7.7 mySubnet ที่สร้างเสร็จแล้ว'))
add(SUB('ส่วน C: สร้างและผูก Internet Gateway'))
add(STEP('7.8', 'ที่เมนูด้านซ้าย เลือก **Internet gateways** จะเห็น IGW ของ Default VPC (Attached) '
                'แล้วคลิก **Create internet gateway**'))
add(IMG(photo('22'), 'รูปที่ 7.8 หน้า Internet gateways'))
add(STEP('7.9', 'ตั้ง Name tag = **myIGW** แล้วคลิก **Create internet gateway**'))
add(IMG(photo('23', 0), 'รูปที่ 7.9 หน้า Create internet gateway'))
add(STEP('7.10', 'myIGW (igw-01c61735301f15317) จะแสดงในรายการโดยมีสถานะ **Detached** คือยังไม่ได้เชื่อมกับ VPC ใด'))
add(IMG(photo('23', 1), 'รูปที่ 7.10 myIGW สถานะ Detached'))
add(STEP('7.11', 'ติ๊กเลือก myIGW → **Actions** → **Attach to VPC**'))
add(IMG(photo('24'), 'รูปที่ 7.11 เลือก myIGW แล้วไปที่ Actions'))
add(STEP('7.12', 'ที่ Available VPCs เลือก **vpc-0d2baa5b377dfd013** (myVPC) แล้วคลิก **Attach internet gateway** '
                 'สถานะของ myIGW จะเปลี่ยนเป็น **Attached** (1 VPC มี IGW ได้เพียง 1 อัน)'))
add(IMG(photo('25'), 'รูปที่ 7.12 Attach myIGW เข้ากับ myVPC'))
add(SUB('ส่วน D: สร้าง Route Table และเพิ่มเส้นทางออกอินเทอร์เน็ต'))
add(STEP('7.13', 'ที่เมนูด้านซ้าย เลือก **Route tables** แล้วคลิก **Create route table**'))
add(IMG(photo('26'), 'รูปที่ 7.13 หน้า Route tables'))
add(STEP('7.14', 'ตั้ง Name = **myRT** และ VPC = **vpc-0d2baa5b377dfd013 (myVPC)** แล้วคลิก **Create route table**'))
add(IMG(photo('27', 0), 'รูปที่ 7.14 หน้า Create route table'))
add(STEP('7.15', 'myRT (rtb-01d4c07b4ab3c9ac5) จะแสดงในรายการโดย Main = **No** สังเกตว่ามี Route table อีกอันของ myVPC '
                 '(rtb-00648948c3331127b, Main = Yes) ซึ่ง AWS สร้างให้อัตโนมัติตอนสร้าง VPC และมีเพียงเส้นทาง local'))
add(IMG(photo('27', 1), 'รูปที่ 7.15 myRT ที่สร้างเสร็จแล้ว'))
add(STEP('7.16', 'ติ๊กเลือก myRT → **Actions** → **Edit routes**'))
add(IMG(photo('28'), 'รูปที่ 7.16 เมนู Actions > Edit routes'))
add(STEP('7.17', 'จะมีเส้นทางเดิม **10.0.0.0/16 → local** (ให้เครื่องใน VPC คุยกันได้ ลบไม่ได้) ให้คลิก **Add route** แล้วตั้งค่า '
                 'Destination = **0.0.0.0/0** (ทุกปลายทางที่ไม่ใช่ใน VPC), Target = **Internet Gateway** → '
                 '**igw-01c61735301f15317** (myIGW) แล้วคลิก **Save changes**'))
add(IMG(photo('29'), 'รูปที่ 7.17 เพิ่มเส้นทาง 0.0.0.0/0 ไปยัง myIGW'))
add(BOX('**ถ้าไม่เห็น IGW ในช่อง Target:** ตรวจสอบว่า Attach myIGW เข้ากับ myVPC แล้ว (ขั้นตอนที่ 7.12) '
        'เพราะ Route table จะเลือกได้เฉพาะ IGW ที่ผูกกับ VPC เดียวกัน'))
add(STEP('7.18', 'ติ๊กเลือก myRT → **Actions** → **Set main route table** แล้วยืนยัน เพื่อให้ myRT เป็น Route table หลักของ myVPC '
                 'Subnet ที่ไม่ได้ผูกกับ Route table ใดโดยตรง (เช่น mySubnet) จะใช้ Route table หลักนี้ จึงออกอินเทอร์เน็ตผ่าน myIGW ได้'))
add(IMG(photo('30'), 'รูปที่ 7.18 Set main route table'))
add(BOX('**อีกวิธีหนึ่ง:** แทนที่จะตั้งเป็น Main route table สามารถใช้ **Actions** → **Edit subnet associations** → ติ๊ก '
        '**mySubnet** → Save associations ได้ วิธีนี้เหมาะเมื่อ VPC มีทั้ง Public และ Private subnet '
        'เพราะผูกเส้นทางออกอินเทอร์เน็ตเฉพาะ Subnet ที่ต้องการ'))
add(SUB('ส่วน E: สร้าง EC2 ใน myVPC และทดสอบ'))
add(STEP('7.19', 'ไปที่ EC2 → **Instances** → **Launch instances** จะเข้าสู่หน้า Launch an instance '
                 '(ค่าเริ่มต้นเป็น Amazon Linux และ t3.micro ต้องเปลี่ยน)'))
add(IMG(photo('31'), 'รูปที่ 7.19 หน้า Launch an instance'))
add(STEP('7.20', 'ตั้งค่าส่วนบนเหมือน Part 1: AMI = **Microsoft Windows Server 2025 Base**, Instance type = เปิด All generations → '
                 '**m7i-flex.large**'))
add(IMG(photo('32', 0), 'รูปที่ 7.20 เลือก Windows Server 2025 และ m7i-flex.large'))
add(STEP('7.21', 'ตั้งค่า Key pair และ Network settings (คลิก **Edit** ที่ Network settings ก่อน)'))
add(BUL('Key pair: **MyKPuseast2**'))
add(BUL('VPC: **vpc-0d2baa5b377dfd013 (myVPC)**'))
add(BUL('Subnet: **mySubnet** (subnet-096ebe4b829069873, us-east-1a, 10.0.1.0/24)'))
add(BUL('Auto-assign public IP: **Enable** (ต้องเปลี่ยนเอง เพราะ mySubnet ตั้งค่าเริ่มต้นเป็น No ถ้าไม่เปิดเครื่องจะไม่มี Public IP)'))
add(BUL('Firewall: **Create security group** ชื่อ **mySG2myVPC** (Description ใช้ค่าที่ระบบตั้งให้)'))
add(BUL('Security group rule 1: Type **rdp** (TCP 3389), Source type **Anywhere** (0.0.0.0/0)'))
add(BUL('คลิก **Add security group rule** → rule 2: Type **All ICMP - IPv4**, Source type **Anywhere** (0.0.0.0/0) '
        'เพื่อให้ ping เครื่องได้'))
add(IMG(photo('32', 1), 'รูปที่ 7.21 เลือก myVPC, mySubnet และสร้าง Security group mySG2myVPC'))
add(BOX('**ทำไมต้องสร้าง Security Group ใหม่:** Security Group ผูกอยู่กับ VPC ที่สร้างมัน MySGuseast2 อยู่ใน Default VPC '
        'จึงเลือกใช้กับเครื่องใน myVPC ไม่ได้ ต้องสร้างใหม่ใน myVPC'))
add(STEP('7.22', 'เลื่อนลงมาตรวจสอบ rule ทั้ง 2 อัน (คำเตือนสีเหลืองเรื่อง 0.0.0.0/0 ใช้ได้สำหรับแลป) '
                 'Storage = **30 GiB gp3** แล้วคลิก **Launch instance**'))
add(IMG(photo('32', 2), 'รูปที่ 7.22 ตรวจสอบ Security group rules และ Storage'))
add(STEP('7.23', 'รอจน Status check เป็น 3/3 checks passed แล้วติ๊กเลือก instance → **Connect** → แท็บ **RDP** → '
                 'Download RDP shortcut file → เปิดไฟล์ → **Connect** (หน้า Connect จะแสดงว่าเครื่องอยู่ใน myVPC, mySubnet '
                 'และ mySG2myVPC) จากนั้นขอรหัสผ่านด้วย **Get Windows password** และไฟล์ MyKPuseast2.pem '
                 'แล้วล็อกอินเหมือน Part 1 ขั้นตอนที่ 3.10–3.16'))
add(IMG(photo('33'), 'รูปที่ 7.23 เชื่อมต่อ RDP เข้าเครื่องใน myVPC'))
add(STEP('7.24', 'ในหน้าต่าง Remote Desktop เปิด **Windows Security** → **Firewall & network protection** แล้วปิด Firewall ของ '
                 '**Private network** และ **Public network (active)** เหตุผลคือ Windows Firewall บล็อก ICMP (ping) ขาเข้าเป็นค่าเริ่มต้น '
                 'แม้ Security Group จะเปิด ICMP ไว้แล้วก็ตาม'))
add(IMG(photo('34'), 'รูปที่ 7.24 ปิด Windows Firewall ของ Private และ Public network'))
add(STEP('7.25', 'ที่หน้า Instances คัดลอก **Public IPv4 address** ของเครื่อง (100.58.220.200) แล้วเปิด **Command Prompt '
                 'บนคอมพิวเตอร์ของเราเอง** และพิมพ์คำสั่ง'))
add(CODE('ping 100.58.220.200'))
add(P('ถ้าได้ **Reply from 100.58.220.200** ครบ 4 ครั้ง (Lost = 0) แสดงว่า VPC ที่สร้างเองทำงานถูกต้อง คือทราฟฟิกจากอินเทอร์เน็ต '
      'เข้ามาทาง myIGW → myRT → mySubnet → เครื่อง และผ่าน Security Group กับ Windows Firewall ได้ '
      'สังเกตว่าเครื่องได้ Private IP **10.0.1.5** ซึ่งอยู่ในช่วงของ mySubnet (10.0.1.0/24)'))
add(IMG(photo('35'), 'รูปที่ 7.25 ping เครื่องใน myVPC จากคอมพิวเตอร์ของเราสำเร็จ'))
add(BOX('**ถ้า ping ไม่ได้ (Request timed out) ให้ตรวจสอบตามลำดับนี้**'))
add(BUL('myIGW สถานะ Attached กับ myVPC'))
add(BUL('myRT มีเส้นทาง 0.0.0.0/0 → myIGW และเป็น Main route table (หรือผูกกับ mySubnet แล้ว)'))
add(BUL('เครื่องมี Public IPv4 address (ถ้าเป็น "–" แปลว่าลืมเปิด Auto-assign public IP ต้องสร้างเครื่องใหม่หรือผูก Elastic IP)'))
add(BUL('Security Group mySG2myVPC มี rule All ICMP - IPv4'))
add(BUL('Windows Firewall ของเครื่องปิดอยู่'))

# ---------- 8. Homework ----------
add(H('8. Homework'))
add(SUB('วัตถุประสงค์'))
add(P('การบ้านนี้นำความรู้จากหัวข้อที่ 6 และ 7 มาใช้ร่วมกัน โดยสร้างเครือข่ายที่ใหญ่ขึ้น ได้แก่ VPC 1 อันที่มี **2 Subnet อยู่คนละ '
      'Availability Zone (AZ)** แต่ละ Subnet มี EC2 2 เครื่อง (รวม 4 เครื่อง) ทุกเครื่องได้ Public IP แบบคงที่จาก Elastic IP '
      'แล้วทดสอบว่าเครื่องทั้ง 4 ถูก ping ได้จากอินเทอร์เน็ต และ ping หากันได้เองข้าม Subnet และข้าม AZ'))
add(P('การวางเครื่องไว้คนละ AZ ช่วยให้ระบบทนต่อความเสียหาย เพราะ AZ คือศูนย์ข้อมูลที่แยกจากกันทางกายภาพ '
      'ถ้า AZ หนึ่งมีปัญหา เครื่องใน AZ อื่นยังทำงานต่อได้'))
add(TABLE(['ส่วนประกอบ', 'ชื่อ', 'ค่าที่ใช้'],
          [['VPC', 'homeworkVPC', '10.0.0.0/16'],
           ['Subnet 1', 'homeworkSubnet1', '10.0.1.0/24 ที่ us-east-1a'],
           ['Subnet 2', 'homeworkSubnet2', '10.0.2.0/24 ที่ us-east-1f'],
           ['Internet Gateway', 'homeworkGateway', 'Attach กับ homeworkVPC'],
           ['Route Table', 'homeworkRoutetable', '0.0.0.0/0 → homeworkGateway, ผูกกับทั้ง 2 Subnet'],
           ['EC2 ใน Subnet 1', 'hwIns1-1, hwIns1-2', 'Windows Server 2025, m7i-flex.large'],
           ['EC2 ใน Subnet 2', 'hwIns2-1, hwIns2-2', 'Windows Server 2025, m7i-flex.large'],
           ['Elastic IP', '4 IP', 'ผูกเครื่องละ 1 IP']],
          [2200, 2800, 4000]))
add(SUB('ส่วน A: สร้าง VPC'))
add(STEP('8.1', 'ไปที่ **VPC** → **Your VPCs** → **Create VPC** แล้วตั้งค่าเหมือนหัวข้อที่ 7 แล้วคลิก **Create VPC**'))
add(BUL('Resources to create: **VPC only**'))
add(BUL('Name tag: **homeworkVPC**'))
add(BUL('IPv4 CIDR: **IPv4 CIDR manual input** → **10.0.0.0/16**'))
add(BUL('IPv6 CIDR block: **No IPv6 CIDR block**, Tenancy: **Default**, VPC encryption control: **None**'))
add(IMG(photo('36'), 'รูปที่ 8.1 ตั้งค่า homeworkVPC'))
add(STEP('8.2', 'จะขึ้นข้อความ **You successfully created vpc-09c34feacc5178271 / homeworkVPC** และ homeworkVPC แสดงในรายการ '
                'สถานะ Available'))
add(IMG(photo('37'), 'รูปที่ 8.2 homeworkVPC ที่สร้างเสร็จแล้ว'))
add(BOX('**หมายเหตุ:** ใช้ CIDR 10.0.0.0/16 ซ้ำกับ myVPC ในหัวข้อที่ 7 ได้ เพราะแต่ละ VPC แยกขาดจากกัน '
        '(ในรูปที่ 8.2 ลบ myVPC ไปแล้ว จึงเหลือแค่ Default VPC และ homeworkVPC) '
        'แต่ถ้าในอนาคตต้องการเชื่อม 2 VPC เข้าด้วยกัน (VPC Peering) ช่วง IP ต้องไม่ซ้ำกัน'))
add(SUB('ส่วน B: สร้าง 2 Subnet คนละ Availability Zone'))
add(STEP('8.3', 'ไปที่ **Subnets** → **Create subnet** แล้วตั้งค่า Subnet แรก แล้วคลิก **Create subnet**'))
add(BUL('VPC ID: **vpc-09c34feacc5178271 (homeworkVPC)**'))
add(BUL('Subnet name: **homeworkSubnet1**'))
add(BUL('Availability Zone: **United States (N. Virginia) / use1-az1 (us-east-1a)**'))
add(BUL('IPv4 VPC CIDR block: **10.0.0.0/16**, IPv4 subnet CIDR block: **10.0.1.0/24**'))
add(IMG(photo('38'), 'รูปที่ 8.3 ตั้งค่า homeworkSubnet1 ที่ us-east-1a'))
add(STEP('8.4', 'กด **Create subnet** อีกครั้งเพื่อสร้าง Subnet ที่สอง โดย**เลือก AZ คนละอันกับ Subnet แรก** '
                'และใช้ช่วง IP ที่ไม่ซ้ำกัน'))
add(BUL('VPC ID: **vpc-09c34feacc5178271 (homeworkVPC)**'))
add(BUL('Subnet name: **homeworkSubnet2**'))
add(BUL('Availability Zone: **United States (N. Virginia) / use1-az5 (us-east-1f)**'))
add(BUL('IPv4 subnet CIDR block: **10.0.2.0/24**'))
add(IMG(photo('39'), 'รูปที่ 8.4 ตั้งค่า homeworkSubnet2 ที่ us-east-1f'))
add(STEP('8.5', 'รายการ Subnets จะมี **homeworkSubnet1** (subnet-0b8c1ee3e70362131) และ **homeworkSubnet2** '
                '(subnet-0a3db1b8d6f898a8b) อยู่ใน homeworkVPC'))
add(IMG(photo('40'), 'รูปที่ 8.5 Subnet ทั้ง 2 อันที่สร้างเสร็จแล้ว'))
add(BOX('**ข้อควรระวัง:** ช่วง IP ของ 2 Subnet ใน VPC เดียวกันต้องไม่ทับกัน ถ้าใส่ 10.0.1.0/24 ซ้ำจะสร้างไม่ได้ '
        'ส่วน 1 Subnet อยู่ได้เพียง 1 AZ เท่านั้น ถ้าต้องการกระจายเครื่องไปหลาย AZ ต้องสร้าง Subnet แยกตาม AZ'))
add(SUB('ส่วน C: สร้างและผูก Internet Gateway'))
add(STEP('8.6', 'ไปที่ **Internet gateways** → **Create internet gateway** ตั้ง Name tag = **homeworkGateway** '
                'แล้วคลิก **Create internet gateway**'))
add(IMG(photo('41'), 'รูปที่ 8.6 สร้าง homeworkGateway'))
add(STEP('8.7', 'homeworkGateway (igw-0bcfccf6f9cb83119) จะมีสถานะ **Detached** ให้ติ๊กเลือกแล้วไปที่ **Actions** → '
                '**Attach to VPC**'))
add(IMG(photo('42'), 'รูปที่ 8.7 เมนู Actions > Attach to VPC'))
add(STEP('8.8', 'ที่ Available VPCs เลือก **vpc-09c34feacc5178271** (homeworkVPC) แล้วคลิก **Attach internet gateway**'))
add(IMG(photo('43'), 'รูปที่ 8.8 Attach homeworkGateway เข้ากับ homeworkVPC'))
add(SUB('ส่วน D: สร้าง Route Table'))
add(STEP('8.9', 'ไปที่ **Route tables** → **Create route table** ตั้ง Name = **homeworkRoutetable** และ VPC = '
                '**vpc-09c34feacc5178271 (homeworkVPC)** แล้วคลิก **Create route table**'))
add(IMG(photo('44'), 'รูปที่ 8.9 สร้าง homeworkRoutetable'))
add(STEP('8.10', 'ติ๊กเลือก homeworkRoutetable (rtb-071532e0bdf6dfb90, Main = No) → **Actions** → **Edit routes**'))
add(IMG(photo('45'), 'รูปที่ 8.10 เมนู Actions > Edit routes'))
add(STEP('8.11', 'คลิก **Add route** แล้วตั้ง Destination = **0.0.0.0/0**, Target = **Internet Gateway** → '
                 '**igw-0bcfccf6f9cb83119 (homeworkGateway)** แล้วคลิก **Save changes**'))
add(IMG(photo('46'), 'รูปที่ 8.11 เพิ่มเส้นทาง 0.0.0.0/0 ไปยัง homeworkGateway'))
add(BOX('**ต่างจากหัวข้อที่ 7:** ครั้งนี้ไม่ได้ตั้ง homeworkRoutetable เป็น Main route table แต่จะผูกกับแต่ละ Subnet โดยตรง '
        'ในขั้นตอนที่ 8.17 ถ้าลืมผูก Subnet จะใช้ Main route table ที่มีแค่เส้นทาง local และเข้าถึงจากอินเทอร์เน็ตไม่ได้'))
add(SUB('ส่วน E: สร้าง EC2 จำนวน 4 เครื่อง'))
add(STEP('8.12', 'ไปที่ EC2 → **Launch instances** สร้างเครื่องแรกใน Subnet 1 ตั้งค่าส่วนบนดังนี้'))
add(BUL('Name: **hwIns1-1**'))
add(BUL('AMI: **Microsoft Windows Server 2025 Base**'))
add(BUL('Instance type: เปิด All generations → **m7i-flex.large**'))
add(IMG(photo('47.1'), 'รูปที่ 8.12 ตั้งค่าส่วนบนของ hwIns1-1'))
add(STEP('8.13', 'ตั้งค่า Key pair และ Network settings (คลิก **Edit** ที่ Network settings ก่อน) แล้วคลิก **Launch instance**'))
add(BUL('Key pair: **MyKPuseast2**'))
add(BUL('VPC: **vpc-09c34feacc5178271 (homeworkVPC)**'))
add(BUL('Subnet: **homeworkSubnet1** (subnet-0b8c1ee3e70362131, us-east-1a)'))
add(BUL('Auto-assign public IP: **Disable** (จะใช้ Elastic IP แทนในขั้นตอนที่ 8.16)'))
add(BUL('Firewall: **Create security group** ชื่อ **hwVPC1**'))
add(BUL('Security group rule 1: Type **rdp** (TCP 3389), Source type **Anywhere** (0.0.0.0/0)'))
add(BUL('Security group rule 2: Type **All ICMP - IPv4**, Source type **Custom**, Source **0.0.0.0/0**'))
add(BUL('Storage: **30 GiB gp3**'))
add(IMG(photo('47.2'), 'รูปที่ 8.13 ตั้งค่า Network settings ของ hwIns1-1'))
add(STEP('8.14', 'ทำซ้ำขั้นตอนที่ 8.12–8.13 อีก 3 เครื่อง โดยเปลี่ยนเฉพาะค่าตามตาราง ค่าอื่นเหมือนเดิมทุกอย่าง'))
add(TABLE(['เครื่อง', 'Subnet', 'Availability Zone', 'Security group'],
          [['hwIns1-1', 'homeworkSubnet1', 'us-east-1a', 'hwVPC1'],
           ['hwIns1-2', 'homeworkSubnet1', 'us-east-1a', 'hwVPC2'],
           ['hwIns2-1', 'homeworkSubnet2', 'us-east-1f', 'hwVPC3'],
           ['hwIns2-2', 'homeworkSubnet2', 'us-east-1f', 'hwVPC4']],
          [2000, 2600, 2200, 2200]))
add(IMG(photo('48.1'), 'รูปที่ 8.14 ตั้งค่าส่วนบนของ hwIns1-2'))
add(IMG(photo('48.2'), 'รูปที่ 8.15 ตั้งค่า Network settings ของ hwIns1-2 (homeworkSubnet1)'))
add(BOX('**ชื่อ Security group ห้ามซ้ำกันใน VPC เดียวกัน:** ในรูปที่ 8.15 ช่อง Security group name ยังเป็น hwVPC1 '
        'ซึ่งซ้ำกับของ hwIns1-1 ต้องเปลี่ยนเป็น **hwVPC2** ก่อนกด Launch (รูปที่ 8.20 แสดงว่าเครื่องนี้ใช้ hwVPC2) '
        'อีกวิธีที่ง่ายกว่าคือเลือก **Select existing security group** → **hwVPC1** ให้ทุกเครื่องใช้ Security group เดียวกัน'))
add(IMG(photo('49.1'), 'รูปที่ 8.16 ตั้งค่าส่วนบนของ hwIns2-1'))
add(IMG(photo('49.2'), 'รูปที่ 8.17 ตั้งค่า Network settings ของ hwIns2-1 (homeworkSubnet2, us-east-1f)'))
add(IMG(photo('50.1'), 'รูปที่ 8.18 ตั้งค่าส่วนบนของ hwIns2-2'))
add(IMG(photo('50.2'), 'รูปที่ 8.19 ตั้งค่า Network settings ของ hwIns2-2 (homeworkSubnet2, us-east-1f)'))
add(STEP('8.15', 'หน้า Instances จะมี 4 เครื่อง สถานะ Running โดย 2 เครื่องอยู่ us-east-1a และ 2 เครื่องอยู่ us-east-1f '
                 'สังเกตว่าคอลัมน์ Public IPv4 address เป็น "–" ทุกเครื่อง เพราะปิด Auto-assign public IP ไว้'))
add(IMG(photo('51'), 'รูปที่ 8.20 EC2 ทั้ง 4 เครื่องใน 2 Subnet'))
add(SUB('ส่วน F: ผูก Elastic IP ให้ทุกเครื่อง'))
add(STEP('8.16', 'ไปที่ **Elastic IPs** แล้ว **Allocate Elastic IP address** จำนวน 4 IP (วิธีเดียวกับหัวข้อที่ 6 ขั้นตอนที่ 6.6–6.8) '
                 'จากนั้นเลือกทีละ IP → **Actions** → **Associate Elastic IP address** → Resource type = **Instance** → '
                 'เลือกเครื่อง → **Associate** จนครบทั้ง 4 เครื่อง'))
add(IMG(photo('52'), 'รูปที่ 8.21 ผูก Elastic IP 34.232.149.75 กับ hwIns1-1 (i-048d2cc2be7c24bb7)'))
add(P('เมื่อเสร็จแล้ว ทุกเครื่องจะมี Public IPv4 address เท่ากับ Elastic IP ของตัวเอง'))
add(TABLE(['เครื่อง', 'Instance ID', 'Private IP', 'Elastic IP'],
          [['hwIns1-1', 'i-048d2cc2be7c24bb7', '10.0.1.228', '34.232.149.75'],
           ['hwIns1-2', 'i-046956f9ddf24fb53', '10.0.1.12', '34.195.199.231'],
           ['hwIns2-1', 'i-07c6f217c664e61d7', '10.0.2.249', '3.212.4.216'],
           ['hwIns2-2', 'i-0a676d5e957bb3f18', '10.0.2.215', '52.87.0.235']],
          [1800, 2800, 2000, 2400]))
add(IMG(photo('53'), 'รูปที่ 8.22 ทุกเครื่องได้ Elastic IP'))
add(SUB('ส่วน G: ผูก Route Table กับ Subnet'))
add(STEP('8.17', 'ไปที่ VPC → **Subnets** ติ๊กเลือก **homeworkSubnet1** → **Actions** → **Edit route table association** '
                 'เลือก Route table ID = **rtb-071532e0bdf6dfb90 (homeworkRoutetable)** ตรวจสอบว่า Routes แสดง '
                 '10.0.0.0/16 → local และ 0.0.0.0/0 → igw-0bcfccf6f9cb83119 แล้วคลิก **Save** '
                 'จากนั้น**ทำซ้ำกับ homeworkSubnet2**'))
add(IMG(photo('54'), 'รูปที่ 8.23 ผูก homeworkRoutetable กับ homeworkSubnet1'))
add(BOX('**ลำดับขั้นตอน:** ในแลปนี้ผูก Route table หลังสร้างเครื่องและผูก Elastic IP แล้ว ซึ่งทำได้เพราะ Route table มีผลทันที '
        'แต่ถ้าทำซ้ำ แนะนำให้ผูก Route table กับ Subnet ตั้งแต่ส่วน D เพื่อให้เชื่อมต่อเครื่องได้ทันทีหลัง Launch'))
add(SUB('ส่วน H: เชื่อมต่อและทดสอบ'))
add(STEP('8.18', 'เชื่อมต่อ RDP เข้าทั้ง 4 เครื่อง (ขอรหัสผ่านแต่ละเครื่องด้วย **Get Windows password** และ MyKPuseast2.pem '
                 'เหมือน Part 1 ขั้นตอนที่ 3.7–3.16 เพราะแต่ละเครื่องมีรหัสผ่านต่างกัน) ชื่อหน้าต่าง Remote Desktop '
                 'จะแสดงชื่อเครื่องและ Public DNS ที่มาจาก Elastic IP เช่น hwIns1-1 – ec2-34-232-149-75.compute-1.amazonaws.com'))
add(IMG(photo('55'), 'รูปที่ 8.24 เชื่อมต่อ RDP เข้าทั้ง 4 เครื่อง'))
add(STEP('8.19', 'ในแต่ละเครื่อง ปิด **Windows Firewall** (Windows Security → Firewall & network protection → ปิด Private และ '
                 'Public network) เพื่อให้ตอบ ping ได้ เหมือนหัวข้อที่ 7 ขั้นตอนที่ 7.24 '
                 'ในรูปที่ 8.25 จะเห็นว่าทุกเครื่องติดตั้ง XAMPP และ Start Apache กับ MySQL ไว้ด้วย (วิธีติดตั้งเหมือน Part 1 หัวข้อที่ 4)'))
add(STEP('8.20', 'ทดสอบ ping **จากคอมพิวเตอร์ของเราเอง** ไปยัง Elastic IP ของทั้ง 4 เครื่อง'))
add(CODE('ping 34.232.149.75'))
add(CODE('ping 34.195.199.231'))
add(CODE('ping 52.87.0.235'))
add(CODE('ping 3.212.4.216'))
add(P('ทุกเครื่องตอบ **Reply from ...** ครบ 4 ครั้ง (Lost = 0) แสดงว่าทราฟฟิกจากอินเทอร์เน็ตเข้าถึงเครื่องในทั้ง 2 Subnet ได้ '
      'ผ่าน homeworkGateway และ homeworkRoutetable (ค่า time ประมาณ 250–270 ms เพราะเครื่องอยู่ที่สหรัฐอเมริกา)'))
add(IMG(photo('56'), 'รูปที่ 8.25 ping จากคอมพิวเตอร์ของเราไปยังทั้ง 4 เครื่องสำเร็จ'))
add(BOX('**หมายเหตุ:** ในรูปที่ 8.25 การ ping hwIns1-1 (34.232.149.75) ครั้งแรกขึ้น **Request timed out** ทั้ง 4 ครั้ง '
        'แต่ครั้งที่สองตอบกลับครบ ในรูปไม่ได้แสดงสาเหตุ แต่ที่พบบ่อยคือยังไม่ได้ปิด Windows Firewall ของเครื่องนั้น '
        'หรือ Route table ยังไม่ได้ผูกกับ Subnet ถ้าเจอให้ตรวจสอบตาม checklist ท้ายหัวข้อที่ 7 แล้ว ping ใหม่'))
add(STEP('8.21', 'ทดสอบ ping **ระหว่างเครื่องด้วยกัน** โดยเปิด Command Prompt ในแต่ละเครื่องแล้ว ping Elastic IP ของเครื่องอื่น'))
add(TABLE(['ping จาก', 'ไปยัง', 'ผลลัพธ์'],
          [['hwIns1-1 (Subnet 1, us-east-1a)', 'hwIns1-2 – 34.195.199.231', 'สำเร็จ – Subnet เดียวกัน'],
           ['hwIns1-2 (Subnet 1, us-east-1a)', 'hwIns2-1 – 3.212.4.216', 'สำเร็จ – ข้าม Subnet และข้าม AZ'],
           ['hwIns2-2 (Subnet 2, us-east-1f)', 'hwIns1-1 – 34.232.149.75', 'สำเร็จ – ข้าม Subnet และข้าม AZ'],
           ['hwIns2-1 (Subnet 2, us-east-1f)', 'hwIns2-2 – 52.87.0.235', 'สำเร็จ – Subnet เดียวกัน']],
          [3200, 3000, 2800]))
add(IMG(photo('57'), 'รูปที่ 8.26 ping ระหว่างเครื่องทั้ง 4 เครื่องสำเร็จ'))
add(P('สังเกตว่า ping ระหว่างเครื่องใช้เวลา **น้อยกว่า 1 ms** (เทียบกับ ~250 ms จากคอมพิวเตอร์ของเรา) และ TTL = 127 '
      'เพราะทราฟฟิกวิ่งอยู่ภายในเครือข่ายของ AWS ทั้งหมด ไม่ได้ออกไปอินเทอร์เน็ตจริง'))
add(BOX('**ping ด้วย Private IP ก็ได้:** เครื่องใน VPC เดียวกันคุยกันผ่านเส้นทาง **10.0.0.0/16 → local** ได้โดยตรง '
        'เช่น จาก hwIns1-1 ใช้คำสั่ง ping 10.0.2.249 (hwIns2-1) ได้โดยไม่ต้องใช้ Elastic IP '
        'วิธีนี้เหมาะกับการสื่อสารภายในระบบมากกว่า เพราะไม่ต้องเปิดเครื่องให้อินเทอร์เน็ตเข้าถึง'))
add(SUB('ส่วน I: คืนทรัพยากร (Clean up)'))
add(STEP('8.22', 'เมื่อทำเสร็จ ให้คืนทรัพยากรตามลำดับนี้เพื่อไม่ให้เสีย credit ของ AWS Academy', keep_next=False))
add(BUL('Disassociate และ Release Elastic IP ทั้ง 4 IP (หัวข้อที่ 6 ขั้นตอนที่ 6.15–6.16)'))
add(BUL('Terminate EC2 ทั้ง 4 เครื่อง'))
add(BUL('ถ้าไม่ใช้ homeworkVPC แล้ว ให้ Detach และ Delete homeworkGateway แล้ว Delete homeworkVPC '
        '(การลบ VPC จะลบ Subnet, Route table และ Security group ที่อยู่ข้างในให้ด้วย)'))

# ---------- Summary ----------
add(H('สรุป Part 2'))
add(SUB('ค่าที่ใช้ในแลปนี้ (ใช้อ้างอิงเมื่อทำซ้ำ)'))
add(TABLE(['รายการ', 'ค่าที่ใช้', 'หมายเหตุ'],
          [['เครื่องทดสอบ Elastic IP', 'Amazon Linux 2023, m7i-flex.large, 8 GiB', 'ไม่มี Key pair, SG MySGuseast2, Default VPC'],
           ['Public IP ปกติ', '34.229.50.79 → 3.81.69.91', 'เปลี่ยนหลัง Stop/Start'],
           ['Elastic IP', '44.196.101.93', 'ไม่เปลี่ยนหลัง Stop/Start, Release แล้ว'],
           ['VPC', 'myVPC (vpc-0d2baa5b377dfd013)', '10.0.0.0/16, VPC only'],
           ['Subnet', 'mySubnet (subnet-096ebe4b829069873)', '10.0.1.0/24, us-east-1a, 251 IP'],
           ['Internet Gateway', 'myIGW (igw-01c61735301f15317)', 'Attach กับ myVPC'],
           ['Route Table', 'myRT (rtb-01d4c07b4ab3c9ac5)', '10.0.0.0/16 → local, 0.0.0.0/0 → myIGW, Main'],
           ['Security Group', 'mySG2myVPC (sg-0be276dccc56f3153)', 'RDP 3389, All ICMP - IPv4'],
           ['Instance ใน myVPC', 'Windows Server 2025, m7i-flex.large', 'Private 10.0.1.5, Public 100.58.220.200'],
           ['Homework VPC', 'homeworkVPC (vpc-09c34feacc5178271)', '10.0.0.0/16, VPC only'],
           ['Homework Subnet', 'homeworkSubnet1 / homeworkSubnet2', '10.0.1.0/24 us-east-1a / 10.0.2.0/24 us-east-1f'],
           ['Homework IGW', 'homeworkGateway (igw-0bcfccf6f9cb83119)', 'Attach กับ homeworkVPC'],
           ['Homework Route Table', 'homeworkRoutetable (rtb-071532e0bdf6dfb90)', '0.0.0.0/0 → IGW, ผูกกับทั้ง 2 Subnet'],
           ['Homework EC2', 'hwIns1-1, hwIns1-2, hwIns2-1, hwIns2-2', 'Windows Server 2025, m7i-flex.large, SG hwVPC1–4'],
           ['Homework Elastic IP', '34.232.149.75, 34.195.199.231, 3.212.4.216, 52.87.0.235',
            'ผูกตามลำดับเครื่องในช่องก่อนหน้า']],
          [2400, 3400, 3200]))
add(SUB('สิ่งที่ควรจำจาก Part 2'))
add(BUL('Public IP ที่ AWS สุ่มให้จะเปลี่ยนทุกครั้งที่ Stop/Start ถ้าต้องการ IP คงที่ให้ใช้ Elastic IP'))
add(BUL('Elastic IP ต้อง Allocate → Associate และเมื่อเลิกใช้ต้อง Disassociate → Release เสมอ เพราะ IP ที่จองไว้มีค่าใช้จ่าย'))
add(BUL('ลำดับการสร้าง VPC เอง: VPC → Subnet → Internet Gateway (Attach) → Route Table (0.0.0.0/0 → IGW) → '
        'ผูก Route Table กับ Subnet → สร้าง EC2'))
add(BUL('Subnet จะเป็น Public subnet ได้ต้องมีเส้นทางไป Internet Gateway และเครื่องต้องมี Public IP'))
add(BUL('ทุก Subnet เสีย IP ให้ AWS 5 IP เช่น /24 ใช้ได้จริง 251 IP'))
add(BUL('Security Group ใช้ได้เฉพาะใน VPC ที่สร้าง ถ้าสร้างเครื่องใน VPC ใหม่ต้องสร้าง Security Group ใหม่'))
add(BUL('การ ping ต้องเปิด ICMP ทั้งใน Security Group และ Windows Firewall'))
add(BUL('1 Subnet อยู่ได้ 1 AZ ถ้าต้องการกระจายเครื่องหลาย AZ ต้องสร้างหลาย Subnet และช่วง IP ของแต่ละ Subnet ต้องไม่ทับกัน'))
add(BUL('Route table ที่ไม่ได้เป็น Main ต้องผูกกับ Subnet เอง (Edit route table association) ไม่อย่างนั้น Subnet จะออกอินเทอร์เน็ตไม่ได้'))
add(BUL('ปิด Auto-assign public IP แล้วใช้ Elastic IP แทนได้ ทำให้ทุกเครื่องมี IP คงที่'))
add(BUL('เครื่องใน VPC เดียวกันคุยกันผ่าน Private IP ได้เสมอ (เส้นทาง local) ไม่ว่าจะอยู่คนละ Subnet หรือคนละ AZ'))
add(PAGEBREAK())

splice_part(UN, 2, ''.join(X), IMG)
