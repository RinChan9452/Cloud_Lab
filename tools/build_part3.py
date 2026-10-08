"""Part 3 content (Thai). Usage: python build_part3.py <unpacked_docx_dir> "D:/Cloud lab/Part 3" """
import sys
from report_lib import H, SUB, P, STEP, BUL, BOX, CODE, TABLE, PAGEBREAK, Images, load_photos, splice_part

UN, PHOTOS = sys.argv[1], sys.argv[2]
photos = load_photos(PHOTOS)
def photo(key, idx=0):
    return photos[key][idx]
IMG = Images(UN, 'part3', docpr_base=3000)

X = []
add = X.append

# ---------- Intro ----------
add(P('Part 3 เป็นการเรียนรู้บริการหน่วยเก็บข้อมูลเสมือน (Virtual Storage) ของ AWS'))
add(BUL('**EBS & EBS snapshot** – ดิสก์เสมือนที่ต่อเข้ากับ EC2 ทดลองสร้าง ต่อเข้าเครื่อง ขยายขนาด ถอดออกแล้วต่อใหม่ '
        'และสำรองข้อมูลด้วย Snapshot'))
add(BUL('**S3** – หน่วยเก็บข้อมูลแบบ Object storage ทดลองสร้าง bucket อัปโหลดไฟล์ เปิดให้สาธารณะอ่านไฟล์ได้ '
        'สร้างโฟลเดอร์ ลบ bucket และใช้ Bucket Versioning เก็บไฟล์หลายเวอร์ชัน'))
add(BOX('**ก่อนเริ่ม:** ทุกขั้นตอนทำใน Region **United States (N. Virginia) us-east-1** และใช้ Key pair **MyKPuseast2** '
        'กับ Security Group **MySGuseast2** จาก Part 1'))

# ---------- 9. EBS & EBS snapshot ----------
add(H('9. EBS & EBS snapshot'))
add(SUB('วัตถุประสงค์'))
add(P('**Amazon EBS (Elastic Block Store)** คือดิสก์เสมือน (Block storage) ที่ต่อเข้ากับ EC2 ทำงานเหมือนฮาร์ดดิสก์ของคอมพิวเตอร์ '
      'ทุก instance มี EBS อย่างน้อย 1 ลูกเป็น **Root volume** ที่เก็บระบบปฏิบัติการ (ไดรฟ์ C:) และเราสร้าง EBS เพิ่มเพื่อเป็น '
      '**Data volume** ได้'))
add(P('จุดสำคัญของ EBS คือ**แยกจาก instance** ข้อมูลใน EBS ยังอยู่แม้จะถอด (Detach) ออกจากเครื่อง และนำไปต่อกับเครื่องอื่นได้ '
      'ขยายขนาดได้โดยไม่ต้องปิดเครื่อง และสำรองข้อมูลได้ด้วย **EBS Snapshot** ซึ่งเก็บสำเนาของ volume ณ เวลาหนึ่งไว้ใน S3 '
      'แล้วนำไปสร้าง volume ใหม่ได้ แม้จะอยู่คนละ Availability Zone'))
add(BOX('**ข้อจำกัดสำคัญ:** EBS volume อยู่ใน Availability Zone (AZ) เดียว และต่อได้เฉพาะกับ instance ที่อยู่ AZ เดียวกันเท่านั้น '
        'ถ้าต้องการย้ายข้อมูลไป AZ อื่น ต้องสร้าง Snapshot แล้วสร้าง volume ใหม่จาก Snapshot ใน AZ ปลายทาง (ส่วน F)'))
add(SUB('ส่วน A: สร้าง Instance และดู Root volume'))
add(STEP('9.1', 'สร้าง EC2 ชื่อ **volumeLab** ด้วยวิธีเดียวกับ Part 1 หัวข้อที่ 3 (Windows Server 2025 Base, **m7i-flex.large**, '
                'Key pair **MyKPuseast2**, Default VPC, Security group **MySGuseast2**, Storage 30 GiB gp3) '
                'เมื่อสร้างเสร็จให้ดูที่แท็บ Details ว่าเครื่องอยู่ **Availability Zone ใด** (ในแลปนี้คือ **us-east-1d**) '
                'เพราะ volume ที่จะสร้างต้องอยู่ AZ เดียวกัน'))
add(IMG(photo('1'), 'รูปที่ 9.1 Instance volumeLab อยู่ที่ us-east-1d'))
add(STEP('9.2', 'ที่เมนูด้านซ้ายของ EC2 เลือก **Elastic Block Store** → **Volumes** จะเห็น Root volume ของ volumeLab '
                '(vol-08555b4460a8d5a77) ขนาด **30 GiB** ชนิด **gp3** สถานะ **In-use** และ Attached resources แสดงว่าต่ออยู่กับ '
                'volumeLab ที่ /dev/sda1 จากนั้นคลิก **Create volume**'))
add(IMG(photo('2'), 'รูปที่ 9.2 Root volume ของ volumeLab'))
add(SUB('ส่วน B: สร้าง EBS volume ใหม่และต่อเข้าเครื่อง'))
add(STEP('9.3', 'ตั้งค่าดังนี้ แล้วคลิก **Create volume**'))
add(BUL('Volume type: **General Purpose SSD (gp3)**'))
add(BUL('Size (GiB): **100**'))
add(BUL('IOPS: **3000** และ Throughput: **125** MiB/s (ค่าเริ่มต้นของ gp3)'))
add(BUL('Availability Zone: **use1-az6 (us-east-1d)** (ต้องตรงกับ AZ ของ volumeLab)'))
add(BUL('Snapshot ID: **Don\'t create volume from a snapshot** (สร้าง volume เปล่า)'))
add(BUL('Encryption: ไม่ต้องติ๊ก'))
add(IMG(photo('3'), 'รูปที่ 9.3 ตั้งค่า volume ใหม่ 100 GiB ที่ us-east-1d'))
add(STEP('9.4', 'จะขึ้นข้อความ **Successfully created volume vol-01f3205f5c3e2ddaa** volume ใหม่มีสถานะ **Available** '
                '(ยังไม่ได้ต่อกับเครื่องใด) ให้ติ๊กเลือก volume นี้ → **Actions** → **Attach volume**'))
add(IMG(photo('4'), 'รูปที่ 9.4 Volume ใหม่สถานะ Available และเมนู Attach volume'))
add(STEP('9.5', 'เลือก Instance = **i-0b9956a1e952c5487 (volumeLab)** ปล่อย Device name เป็น **xvdb** (ค่าที่แนะนำสำหรับ '
                'data volume ของ Windows คือ xvd[f-p]) แล้วคลิก **Attach volume**'))
add(IMG(photo('5'), 'รูปที่ 9.5 Attach volume เข้ากับ volumeLab'))
add(BOX('**ถ้าไม่เห็น instance ในรายการ:** ช่อง Instance จะแสดงเฉพาะเครื่องที่อยู่ **AZ เดียวกับ volume** '
        '(ดูข้อความใต้ช่อง Only instances in the same Availability Zone...) ถ้าสร้าง volume ผิด AZ ต้องลบแล้วสร้างใหม่'))
add(STEP('9.6', 'จะขึ้นข้อความ **Successfully attached volume** และสถานะของ volume เปลี่ยนเป็น **In-use** '
                'Attached resources แสดงว่าต่อกับ volumeLab ที่ xvdb'))
add(IMG(photo('6'), 'รูปที่ 9.6 Volume ใหม่สถานะ In-use'))
add(SUB('ส่วน C: ทำให้ Windows ใช้งานดิสก์ใหม่ได้'))
add(STEP('9.7', 'เชื่อมต่อ RDP เข้า volumeLab (เหมือน Part 1 ขั้นตอนที่ 3.7–3.16) แล้วคลิกขวาที่ปุ่ม Start → **Disk Management** '
                '(หรือกด Win + R แล้วพิมพ์ diskmgmt.msc) จะเห็น **Disk 1** ขนาด 99.98 GB สถานะ **Unallocated** '
                'คือ Windows มองเห็นดิสก์แล้วแต่ยังไม่มี partition จึงยังใช้งานไม่ได้'))
add(IMG(photo('7'), 'รูปที่ 9.7 Disk 1 ขนาด 99.98 GB ยังเป็น Unallocated'))
add(BOX('**ถ้ามีหน้าต่าง Initialize Disk ขึ้นมา:** เลือก **GPT (GUID Partition Table)** แล้วคลิก OK ดิสก์จึงจะเปลี่ยนเป็น Online '
        'และสร้าง partition ได้ ในรูปที่ 9.7 ดิสก์เป็น Basic / Online แล้ว'))
add(STEP('9.8', 'คลิกขวาที่พื้นที่ **Unallocated** ของ Disk 1 → **New Simple Volume** → กด **Next** ไปเรื่อยๆ โดยใช้ค่าเริ่มต้น '
                '(ใช้พื้นที่ทั้งหมด, Drive letter **D**, File system **NTFS**, Volume label New Volume, Quick format) → **Finish** '
                'เมื่อเสร็จ Disk 1 จะเป็น **New Volume (D:) 99.98 GB NTFS** และเปิด File Explorer → This PC จะเห็นไดรฟ์ D:'))
add(IMG(photo('8'), 'รูปที่ 9.8 ไดรฟ์ D: ปรากฏหลังสร้าง partition'))
add(STEP('9.9', 'ทดสอบเขียนข้อมูล: เปิดไดรฟ์ D: คลิกขวา → New → Text Document ตั้งชื่อ **Hello** '
                'ไฟล์นี้จะใช้ตรวจสอบในส่วน E ว่าข้อมูลยังอยู่หลังถอด volume ออกแล้วต่อใหม่'))
add(IMG(photo('9'), 'รูปที่ 9.9 สร้างไฟล์ Hello ในไดรฟ์ D:'))
add(SUB('ส่วน D: ขยายขนาด volume (Modify volume)'))
add(STEP('9.10', 'กลับไปที่ AWS Console → **Volumes** ติ๊กเลือก volume 100 GiB (vol-01f3205f5c3e2ddaa) → **Actions** → '
                 '**Modify volume** (ทำได้ขณะ volume ต่ออยู่และเครื่องเปิดอยู่)'))
add(IMG(photo('10'), 'รูปที่ 9.10 เมนู Actions > Modify volume'))
add(STEP('9.11', 'เปลี่ยน Size (GiB) จาก **100** เป็น **150** (Volume type, IOPS และ Throughput ใช้ค่าเดิม) แล้วคลิก **Modify** '
                 'และยืนยัน'))
add(IMG(photo('11'), 'รูปที่ 9.11 เปลี่ยนขนาดเป็น 150 GiB'))
add(STEP('9.12', 'กลับไปที่ Disk Management ในเครื่อง (คลิก **Action** → **Refresh** หรือ **Rescan Disks** ถ้ายังไม่เห็น) '
                 'Disk 1 จะมีขนาด **149.98 GB** โดยมีพื้นที่ใหม่ **50.00 GB Unallocated** ต่อท้ายไดรฟ์ D:'))
add(IMG(photo('12'), 'รูปที่ 9.12 พื้นที่ใหม่ 50 GB Unallocated'))
add(STEP('9.13', 'คลิกขวาที่พื้นที่ 50 GB → **New Simple Volume** → ใช้ค่าเริ่มต้นจนจบ จะได้ไดรฟ์ใหม่ **New Volume (E:) 50.00 GB** '
                 'และ This PC จะแสดงไดรฟ์ C:, D: และ E:'))
add(IMG(photo('13'), 'รูปที่ 9.13 ไดรฟ์ E: จากพื้นที่ที่ขยายเพิ่ม'))
add(BOX('**อีกวิธีหนึ่ง:** ถ้าต้องการให้ไดรฟ์ D: ใหญ่ขึ้นแทนการสร้างไดรฟ์ใหม่ ให้คลิกขวาที่ **D:** → **Extend Volume** '
        'แล้วเลือกพื้นที่ 50 GB ไดรฟ์ D: จะกลายเป็น 150 GB'))
add(BOX('**ข้อควรรู้เรื่อง Modify volume:** ขยายขนาดได้อย่างเดียว **ลดขนาดไม่ได้** และหลัง Modify แล้วต้องรอประมาณ **6 ชั่วโมง** '
        'จึงจะ Modify volume เดิมได้อีกครั้ง ระหว่างนั้นสถานะจะเป็น In-use - optimizing ซึ่งยังใช้งานได้ตามปกติ'))
add(SUB('ส่วน E: ถอด volume แล้วต่อใหม่ ข้อมูลยังอยู่'))
add(STEP('9.14', 'ที่ **Volumes** ติ๊กเลือก vol-01f3205f5c3e2ddaa (ตอนนี้ Size = 150 GiB สถานะ In-use - optimizing) → **Actions** → '
                 '**Detach volume** → ยืนยัน **Detach**'))
add(IMG(photo('14'), 'รูปที่ 9.14 เมนู Actions > Detach volume'))
add(BOX('**ก่อน Detach ในการใช้งานจริง:** ควรปิดโปรแกรมที่ใช้ไฟล์ในไดรฟ์นั้น และคลิกขวาที่ Disk 1 ใน Disk Management → **Offline** ก่อน '
        'เพื่อให้ Windows เขียนข้อมูลที่ค้างอยู่ลงดิสก์ให้ครบ ป้องกันข้อมูลเสียหาย ห้ามใช้ Force detach volume ถ้าไม่จำเป็น'))
add(STEP('9.15', 'ใน Disk Management และ This PC ของ volumeLab ไดรฟ์ **D: และ E: จะหายไป** เหลือแค่ Disk 0 (ไดรฟ์ C:) '
                 'ส่วนใน AWS Console volume จะกลับเป็นสถานะ Available'))
add(IMG(photo('15'), 'รูปที่ 9.15 ไดรฟ์ D: และ E: หายไปหลัง Detach'))
add(STEP('9.16', 'ติ๊กเลือก volume เดิม (สถานะ **Available**, Attached resources ว่าง) → **Actions** → **Attach volume** → '
                 'เลือก volumeLab แล้วคลิก **Attach volume** เหมือนขั้นตอนที่ 9.5'))
add(IMG(photo('16'), 'รูปที่ 9.16 Attach volume เดิมกลับเข้า volumeLab'))
add(STEP('9.17', 'ใน Disk Management จะเห็น Disk 1 ขนาด 149.98 GB กลับมาพร้อม **New Volume (D:)** และ **New Volume (E:)** '
                 'ทันที โดยไม่ต้องสร้าง partition ใหม่ เพราะข้อมูล partition เก็บอยู่ใน volume'))
add(IMG(photo('17'), 'รูปที่ 9.17 ไดรฟ์ D: และ E: กลับมาหลัง Attach ใหม่'))
add(STEP('9.18', 'เปิดไดรฟ์ D: จะเห็นไฟล์ **Hello** ที่สร้างไว้ในขั้นตอนที่ 9.9 ยังอยู่ครบ แสดงว่าข้อมูลใน EBS ไม่หายเมื่อถอดออกจากเครื่อง '
                 '(volume นี้จึงนำไปต่อกับเครื่องอื่นใน AZ เดียวกันเพื่อย้ายข้อมูลได้)'))
add(IMG(photo('18'), 'รูปที่ 9.18 ไฟล์ Hello ยังอยู่ในไดรฟ์ D:'))
add(SUB('ส่วน F: สำรองข้อมูลด้วย Snapshot และสร้าง volume ใหม่จาก Snapshot'))
add(STEP('9.19', 'ที่เมนูด้านซ้าย เลือก **Elastic Block Store** → **Snapshots** (ตอนนี้ยังไม่มี Snapshot ใน Region นี้) '
                 'แล้วคลิก **Create snapshot**'))
add(IMG(photo('19'), 'รูปที่ 9.19 หน้า Snapshots'))
add(STEP('9.20', 'ตั้งค่าดังนี้ แล้วคลิก **Create snapshot**'))
add(BUL('Resource type: **Volume** (สร้าง Snapshot จาก volume เดียว ถ้าเลือก Instance จะสร้าง Snapshot ของทุก volume ในเครื่อง)'))
add(BUL('Volume ID: **vol-01f3205f5c3e2ddaa** (us-east-1d) คือ volume 150 GiB ที่มีไฟล์ Hello'))
add(BUL('Description: **TestSnapshot**'))
add(IMG(photo('20'), 'รูปที่ 9.20 ตั้งค่า Create snapshot'))
add(STEP('9.21', 'จะขึ้นข้อความ **Successfully created snapshot snap-006e27c18b8c4b275** โดย Volume size = **150 GiB** '
                 'เท่ากับ volume ต้นทาง และ Snapshot status = **Pending** (Progress 0%) ให้รอจนสถานะเป็น **Completed** '
                 '(ใช้เวลาหลายนาทีขึ้นกับปริมาณข้อมูล)'))
add(IMG(photo('21'), 'รูปที่ 9.21 Snapshot สถานะ Pending'))
add(BOX('**Snapshot เป็นแบบ Incremental:** Snapshot แรกจะเก็บเฉพาะ block ที่มีข้อมูลจริง (ไม่ใช่ทั้ง 150 GiB) และ Snapshot ครั้งต่อไป '
        'ของ volume เดิมจะเก็บเฉพาะส่วนที่เปลี่ยนแปลง จึงประหยัดพื้นที่และค่าใช้จ่าย ส่วน Volume size 150 GiB คือขนาดของ volume '
        'ที่จะได้เมื่อนำ Snapshot ไปสร้าง volume ใหม่'))
add(STEP('9.22', 'ไปที่ **Volumes** → **Create volume** แล้วตั้งค่าดังนี้ จากนั้นคลิก **Create volume**'))
add(BUL('Volume type: **General Purpose SSD (gp3)**'))
add(BUL('Snapshot ID: **snap-006e27c18b8c4b275** (Snapshot ที่สร้างในขั้นตอนที่ 9.21)'))
add(BUL('Size (GiB): ต้อง**ไม่น้อยกว่าขนาดของ Snapshot (150 GiB)** volume ใหม่ในแลปนี้ได้ขนาด 150 GiB'))
add(BUL('Availability Zone: **use1-az1 (us-east-1a)** ซึ่ง**ต่างจาก**ต้นทาง (us-east-1d) เพื่อแสดงว่า Snapshot ใช้ย้ายข้อมูลข้าม AZ ได้'))
add(IMG(photo('22'), 'รูปที่ 9.22 สร้าง volume จาก Snapshot ที่ us-east-1a'))
add(BOX('**ข้อความสีแดงเรื่อง Fast snapshot restore:** ในรูปที่ 9.22 ขึ้น **You are not authorized to perform this operation ... '
        'ec2:DescribeFastSnapshotRestores** เพราะบัญชี AWS Academy ไม่มีสิทธิ์ใช้ฟีเจอร์นี้ ไม่กระทบการสร้าง volume ให้ข้ามไปได้'))
add(STEP('9.23', 'จะขึ้นข้อความ **Successfully created volume vol-058841f3897d8a266** ขนาด **150 GiB** ที่ **us-east-1a** '
                 'คอลัมน์ Snapshot ID แสดง snap-006e27c... สถานะเริ่มเป็น Creating แล้วเปลี่ยนเป็น Available '
                 'volume นี้มีข้อมูลเหมือน volume ต้นทาง ณ เวลาที่สร้าง Snapshot (รวมไฟล์ Hello) '
                 'และพร้อมนำไป Attach กับเครื่องใดก็ได้ที่อยู่ใน us-east-1a'))
add(IMG(photo('23'), 'รูปที่ 9.23 Volume ใหม่จาก Snapshot ที่ us-east-1a'))
add(SUB('ส่วน G: คืนทรัพยากร (Clean up)'))
add(STEP('9.24', 'เมื่อทำเสร็จ ให้คืนทรัพยากรเพื่อไม่ให้เสีย credit ของ AWS Academy', keep_next=False))
add(BUL('Detach แล้ว Delete volume ที่สร้างเพิ่ม (vol-01f3205f5c3e2ddaa และ vol-058841f3897d8a266)'))
add(BUL('Delete Snapshot snap-006e27c18b8c4b275 (Snapshots → Actions → Delete snapshot)'))
add(BUL('Terminate instance volumeLab (Root volume จะถูกลบไปพร้อมเครื่องเพราะตั้ง Delete on termination ไว้เป็นค่าเริ่มต้น '
        'แต่ volume ที่สร้างและ Attach เพิ่มเอง**จะไม่ถูกลบอัตโนมัติ** ต้องลบเอง)'))

# ---------- 10. S3 ----------
add(H('10. S3'))
add(SUB('วัตถุประสงค์'))
add(P('**Amazon S3 (Simple Storage Service)** คือหน่วยเก็บข้อมูลแบบ **Object storage** เก็บไฟล์ได้ไม่จำกัดจำนวน '
      'เข้าถึงได้ผ่านอินเทอร์เน็ตด้วย URL โดยไม่ต้องต่อเข้ากับ EC2 เหมือน EBS ข้อมูลถูกเก็บซ้ำหลาย Availability Zone โดยอัตโนมัติ'))
add(TABLE(['คำศัพท์', 'ความหมาย'],
          [['Bucket', 'ที่เก็บ object ชื่อต้อง**ไม่ซ้ำกับใครในโลก** (Global namespace) และอยู่ใน Region เดียว'],
           ['Object', 'ไฟล์ 1 ไฟล์ที่เก็บใน bucket พร้อม metadata เช่น ขนาด วันที่แก้ไข'],
           ['Key', 'ชื่อเต็มของ object เช่น testFolder/SA Project Note.txt'],
           ['Folder', 'ไม่ใช่โฟลเดอร์จริง เป็นแค่ prefix ของ key ที่ลงท้ายด้วย / เพื่อจัดกลุ่ม object'],
           ['Block Public Access / ACL', 'การตั้งค่าที่ควบคุมว่าใครเข้าถึง bucket และ object ได้'],
           ['Versioning', 'เก็บทุกเวอร์ชันของ object เมื่ออัปโหลดไฟล์ชื่อเดิมทับ']],
          [2600, 6400]))
add(SUB('ส่วน A: สร้าง Bucket และอัปโหลดไฟล์'))
add(STEP('10.1', 'พิมพ์ **S3** ในช่อง Search แล้วเลือกบริการ S3 จะเข้าสู่หน้า **Amazon S3** แล้วคลิก **Create bucket**'))
add(IMG(photo('24'), 'รูปที่ 10.1 หน้าแรกของ Amazon S3'))
add(STEP('10.2', 'ตั้งค่าดังนี้ แล้วเลื่อนลงล่างสุดคลิก **Create bucket** (ตอนนี้ตั้งแค่ชื่อ ส่วนการตั้งค่าอื่นใช้ค่าเริ่มต้น และจะแก้ไขในส่วน C)'))
add(BUL('AWS Region: **US East (N. Virginia) us-east-1**'))
add(BUL('Bucket type: **General purpose**'))
add(BUL('Bucket namespace: **Global namespace**'))
add(BUL('Bucket name: **test9452test** (3–63 ตัวอักษร ใช้ได้เฉพาะ a-z, 0-9, จุด และขีด ต้องไม่ซ้ำกับใครในโลก)'))
add(BUL('Object Ownership: **ACLs disabled (recommended)** (ค่าเริ่มต้น)'))
add(BUL('Block Public Access settings: **Block all public access** ติ๊กไว้ (ค่าเริ่มต้น)'))
add(IMG(photo('25'), 'รูปที่ 10.2 ตั้งชื่อ bucket test9452test'))
add(BOX('**ถ้าขึ้นว่าชื่อ bucket ซ้ำ:** ชื่อ bucket ต้องไม่ซ้ำกับทุกบัญชี AWS ทั่วโลก ให้เติมตัวเลขหรือคำอื่นจนกว่าจะไม่ซ้ำ '
        'ชื่อที่ถูกลบไปแล้วอาจมีคนอื่นนำไปใช้ได้'))
add(STEP('10.3', 'จะขึ้นข้อความ **Successfully created bucket "test9452test"** และเข้าสู่หน้า bucket แท็บ **Objects** '
                 'ซึ่งยังไม่มี object ให้คลิก **Upload**'))
add(IMG(photo('26'), 'รูปที่ 10.3 Bucket ใหม่ที่ยังว่าง'))
add(STEP('10.4', 'คลิก **Add files** แล้วเลือกไฟล์ที่จะอัปโหลด (ในแลปนี้คือ **SA Project Note.txt** ขนาด 679 B) '
                 'Destination จะเป็น s3://test9452test แล้วคลิก **Upload**'))
add(IMG(photo('27'), 'รูปที่ 10.4 อัปโหลดไฟล์ SA Project Note.txt'))
add(STEP('10.5', 'กลับมาที่แท็บ Objects จะเห็น **SA Project Note.txt** ชนิด txt ขนาด 679.0 B Storage class **Standard**'))
add(IMG(photo('28'), 'รูปที่ 10.5 Object ที่อัปโหลดแล้ว'))
add(STEP('10.6', 'คลิกชื่อไฟล์เพื่อดูรายละเอียด จะเห็นข้อมูลสำคัญ ได้แก่'))
add(BUL('**S3 URI:** s3://test9452test/SA Project Note.txt (ใช้กับ AWS CLI)'))
add(BUL('**Object URL:** https://test9452test.s3.us-east-1.amazonaws.com/SA+Project+Note.txt (ลิงก์สำหรับเปิดผ่านเบราว์เซอร์)'))
add(BUL('**Bucket Versioning:** Disabled (จะเปิดใช้ในส่วน F)'))
add(IMG(photo('29'), 'รูปที่ 10.6 รายละเอียดของ object'))
add(SUB('ส่วน B: เปิด Object URL ก่อนแก้สิทธิ์'))
add(STEP('10.7', 'คัดลอก **Object URL** ไปเปิดในเบราว์เซอร์ จะขึ้น **AccessDenied** เพราะค่าเริ่มต้นของ S3 คือทุก bucket และ object '
                 'เป็น**ส่วนตัว (private)** มีแต่เจ้าของบัญชีที่เข้าถึงได้'))
add(IMG(photo('41'), 'รูปที่ 10.7 เปิด Object URL ก่อนแก้สิทธิ์ ขึ้น AccessDenied'))
add(SUB('ส่วน C: เปิดให้สาธารณะเข้าถึง bucket'))
add(P('การทำให้คนทั่วไปอ่านไฟล์ได้ต้องแก้ 3 จุดตามลำดับ คือ ปิด Block public access → เปิด ACL → ให้สิทธิ์ Everyone'))
add(STEP('10.8', 'ที่หน้า bucket ไปที่แท็บ **Permissions** จะเห็น **Block all public access: On** และข้อความว่า public access ถูกบล็อก '
                 'ให้คลิก **Edit** ที่หัวข้อ Block public access (bucket settings)'))
add(IMG(photo('30'), 'รูปที่ 10.8 แท็บ Permissions ของ bucket'))
add(STEP('10.9', 'เอาเครื่องหมายออกจาก **Block all public access** (ตัวเลือกย่อยทั้ง 4 จะถูกเอาออกด้วย) แล้วคลิก **Save changes** '
                 'จะมีหน้าต่างให้พิมพ์ **confirm** เพื่อยืนยัน'))
add(IMG(photo('31'), 'รูปที่ 10.9 ปิด Block all public access'))
add(STEP('10.10', 'จะขึ้นข้อความ **Successfully edited Block Public Access settings** เลื่อนลงมาที่ **Object Ownership** จะเห็นว่าเป็น '
                  '**Bucket owner enforced** (ACL ถูกปิด) และปุ่ม Edit ของ Access control list (ACL) กดไม่ได้ '
                  'ให้คลิก **Edit** ที่ Object Ownership'))
add(IMG(photo('32'), 'รูปที่ 10.10 Object Ownership เป็น Bucket owner enforced'))
add(STEP('10.11', 'เปลี่ยนจาก ACLs disabled เป็น **ACLs enabled** → ติ๊ก **I acknowledge that ACLs will be restored** → '
                  'Object Ownership เลือก **Bucket owner preferred** แล้วคลิก **Save changes**'))
add(IMG(photo('33'), 'รูปที่ 10.11 เปิด ACLs enabled'))
add(STEP('10.12', 'จะขึ้นข้อความ **Successfully edited Object Ownership** และปุ่ม **Edit** ของ Access control list (ACL) กดได้แล้ว ให้คลิก Edit'))
add(IMG(photo('34'), 'รูปที่ 10.12 ปุ่ม Edit ของ ACL ใช้งานได้'))
add(STEP('10.13', 'ที่แถว **Everyone (public access)** ติ๊ก **Objects: List** → ติ๊ก **I understand the effects of these changes on my objects '
                  'and buckets** แล้วคลิก **Save changes** (List หมายถึงให้คนทั่วไปดูรายชื่อ object ใน bucket ได้)'))
add(IMG(photo('35'), 'รูปที่ 10.13 ให้ Everyone มีสิทธิ์ List objects'))
add(STEP('10.14', 'จะขึ้นข้อความ **Successfully edited access control list** และแถว Everyone แสดงสิทธิ์ **List** พร้อมคำเตือนสีเหลืองว่า '
                  'AWS ไม่แนะนำให้สิทธิ์ Everyone'))
add(IMG(photo('36'), 'รูปที่ 10.14 ACL ของ bucket หลังแก้ไข'))
add(SUB('ส่วน D: ให้สาธารณะอ่านไฟล์ได้'))
add(STEP('10.15', 'สิทธิ์ List ของ bucket ยังไม่พอให้อ่านเนื้อหาไฟล์ ต้องให้สิทธิ์ที่ตัว object ด้วย: กลับไปที่แท็บ Objects '
                  'คลิกที่ **SA Project Note.txt** → แท็บ **Permissions** จะเห็นว่า Everyone ยังไม่มีสิทธิ์ ให้คลิก **Edit**'))
add(IMG(photo('38'), 'รูปที่ 10.15 แท็บ Permissions ของ object'))
add(STEP('10.16', 'ที่แถว **Everyone (public access)** ติ๊ก **Objects: Read** → ติ๊ก **I understand the effects of these changes on this object** '
                  'แล้วคลิก **Save changes**'))
add(IMG(photo('40'), 'รูปที่ 10.16 ให้ Everyone มีสิทธิ์ Read object'))
add(BOX('**อีกวิธีหนึ่ง:** ที่แท็บ Objects ติ๊กเลือกไฟล์ → **Actions** → **Make public using ACL** (ดูเมนูในรูปที่ 10.20) '
        'จะให้สิทธิ์ Read กับ Everyone ในขั้นตอนเดียว แต่ต้องทำส่วน C ให้เสร็จก่อนเหมือนกัน'))
add(STEP('10.17', 'เปิด **Object URL** เดิมในเบราว์เซอร์อีกครั้ง (กด Refresh) ตอนนี้จะเห็น**เนื้อหาของไฟล์** แทน AccessDenied '
                  'แสดงว่าทุกคนบนอินเทอร์เน็ตอ่านไฟล์นี้ได้แล้ว'))
add(IMG(photo('42'), 'รูปที่ 10.17 เปิด Object URL หลังแก้สิทธิ์ เห็นเนื้อหาไฟล์'))
add(BOX('**ความปลอดภัย:** ทุกคนที่มี URL จะอ่านไฟล์ได้ ใช้เฉพาะไฟล์ที่ตั้งใจเผยแพร่ เช่น รูปภาพหรือไฟล์ของเว็บไซต์ '
        'ห้ามใช้กับไฟล์ที่มีข้อมูลส่วนตัว และหลังทดสอบเสร็จควรเปิด Block all public access กลับ'))
add(SUB('ส่วน E: สร้างโฟลเดอร์ คัดลอกไฟล์ และลบ bucket'))
add(STEP('10.18', 'ที่แท็บ Objects คลิก **Create folder** ตั้ง Folder name = **testFolder** (ห้ามมี /) Server-side encryption ใช้ '
                  '**Don\'t specify an encryption key** แล้วคลิก **Create folder**'))
add(IMG(photo('43'), 'รูปที่ 10.18 สร้างโฟลเดอร์ testFolder'))
add(STEP('10.19', 'จะขึ้นข้อความ **Successfully created folder "testFolder"** และแท็บ Objects มี 2 รายการ คือ SA Project Note.txt '
                  'และ testFolder/ (ชนิด Folder)'))
add(IMG(photo('44'), 'รูปที่ 10.19 โฟลเดอร์ testFolder ที่สร้างเสร็จแล้ว'))
add(STEP('10.20', 'ติ๊กเลือก **SA Project Note.txt** → **Actions** → **Copy** (ถ้าต้องการย้ายไฟล์ไม่ให้เหลือที่เดิม ให้เลือก **Move**)'))
add(IMG(photo('45'), 'รูปที่ 10.20 เมนู Actions > Copy'))
add(STEP('10.21', 'ตั้งค่า Destination type = **General purpose bucket**, Destination = **s3://test9452test/testFolder/** '
                  '(พิมพ์เองหรือกด **Browse S3** เพื่อเลือก) Additional copy settings = **Copy source settings** แล้วคลิก **Copy**'))
add(IMG(photo('46'), 'รูปที่ 10.21 เลือกปลายทางเป็น testFolder'))
add(STEP('10.22', 'เปิดโฟลเดอร์ **testFolder/** จะเห็น SA Project Note.txt อยู่ข้างใน โดย Last modified เป็นเวลาที่คัดลอก (21:05:58) '
                  'เพราะการคัดลอกสร้าง object ใหม่'))
add(IMG(photo('47'), 'รูปที่ 10.22 ไฟล์ที่คัดลอกอยู่ใน testFolder'))
add(STEP('10.23', 'ทดสอบลบ bucket: คลิก **Buckets** ที่ breadcrumb ด้านบน → เลือก **test9452test** → คลิก **Delete**'))
add(IMG(photo('48'), 'รูปที่ 10.23 เลือก bucket แล้วคลิก Delete'))
add(STEP('10.24', 'จะขึ้นข้อความสีแดง **This bucket is not empty – Buckets must be empty before they can be deleted** '
                  'และปุ่ม Delete bucket กดไม่ได้ ต้องลบ object ทั้งหมดก่อน ให้คลิก **Empty bucket**'))
add(IMG(photo('49'), 'รูปที่ 10.24 ลบ bucket ที่ยังมี object ไม่ได้'))
add(STEP('10.25', 'พิมพ์ **permanently delete** ในช่องยืนยัน แล้วคลิก **Empty** (object ทั้งหมดใน bucket จะถูกลบถาวร กู้คืนไม่ได้)'))
add(IMG(photo('50'), 'รูปที่ 10.25 Empty bucket'))
add(STEP('10.26', 'กลับไปลบ bucket อีกครั้ง พิมพ์ชื่อ bucket **test9452test** ในช่องยืนยัน แล้วคลิก **Delete bucket**'))
add(IMG(photo('51'), 'รูปที่ 10.26 ยืนยันการลบ bucket'))
add(STEP('10.27', 'จะขึ้นข้อความ **Successfully deleted bucket "test9452test"** และรายการ General purpose buckets ว่างเปล่า'))
add(IMG(photo('52'), 'รูปที่ 10.27 ลบ bucket สำเร็จ'))
add(SUB('ส่วน F: Bucket Versioning'))
add(STEP('10.28', 'สร้าง bucket ใหม่ชื่อ **test555test** (วิธีเดียวกับขั้นตอนที่ 10.1–10.2 ใช้ค่าเริ่มต้นทั้งหมด) แล้วอัปโหลด '
                  '**SA Project Note.txt** ฉบับเดิม (679 B, Last modified 21:14:07) ในรูปจะเห็นเนื้อหาไฟล์ใน Notepad ด้วย'))
add(IMG(photo('53'), 'รูปที่ 10.28 Bucket test555test และไฟล์ต้นฉบับ'))
add(STEP('10.29', 'ไปที่แท็บ **Properties** ของ bucket จะเห็น **Bucket Versioning: Disabled** ให้คลิก **Edit**'))
add(IMG(photo('54'), 'รูปที่ 10.29 Bucket Versioning ยังเป็น Disabled'))
add(STEP('10.30', 'เลือก **Enable** แล้วคลิก **Save changes**'))
add(IMG(photo('55'), 'รูปที่ 10.30 เปิด Bucket Versioning'))
add(STEP('10.31', 'กลับมาที่แท็บ Objects จะมีสวิตช์ **Show versions** เพิ่มขึ้นมา จากนั้นแก้ไขไฟล์ SA Project Note.txt บนเครื่องของเรา '
                  '(ในแลปนี้เพิ่มบรรทัด "Aoi, Koi, Daidaiiro No Hi") แล้ว**กด Ctrl + S บันทึกไฟล์** โดยใช้ชื่อไฟล์เดิม'))
add(IMG(photo('56'), 'รูปที่ 10.31 แก้ไขไฟล์ต้นฉบับบนเครื่อง'))
add(STEP('10.32', 'คลิก **Upload** → **Add files** → เลือกไฟล์ SA Project Note.txt ที่แก้ไขแล้ว (ชื่อเดิม) → **Upload**'))
add(IMG(photo('57'), 'รูปที่ 10.32 อัปโหลดไฟล์ชื่อเดิมทับ'))
add(BOX('**ข้อสังเกตจากรูป:** ในรูปที่ 10.31 แท็บของ Notepad ยังมีจุด ● (ยังไม่ได้บันทึก) และไฟล์ที่อัปโหลดในรูปที่ 10.32–10.34 '
        'ยังมีขนาด 679 B เท่าเดิม แสดงว่าน่าจะอัปโหลดไฟล์ก่อนบันทึกการแก้ไข ถึงอย่างนั้น S3 ก็ยังสร้างเวอร์ชันใหม่ '
        'เพราะ Versioning สร้างเวอร์ชันใหม่ทุกครั้งที่อัปโหลดชื่อเดิม ไม่ว่าเนื้อหาจะเปลี่ยนหรือไม่ ถ้าทำซ้ำให้บันทึกไฟล์ก่อนอัปโหลด '
        'จะเปิดเวอร์ชันใหม่แล้วเห็นบรรทัดที่เพิ่มได้'))
add(STEP('10.33', 'ในแท็บ Objects ยังเห็นไฟล์เพียง 1 รายการ แต่ **Last modified เปลี่ยนเป็น 21:21:28** (เวลาที่อัปโหลดใหม่)'))
add(IMG(photo('58'), 'รูปที่ 10.33 Last modified เปลี่ยนหลังอัปโหลดทับ'))
add(STEP('10.34', 'คลิกที่ไฟล์ → แท็บ **Versions** จะเห็น **Versions (2)** คือ'))
add(BUL('**K7WtSS7Ae0nJTrmhHYpzV1pGuCwc... (Current version)** – 21:21:28 เวอร์ชันที่อัปโหลดล่าสุด'))
add(BUL('**null** – 21:14:07 เวอร์ชันเดิม Version ID เป็น null เพราะอัปโหลดก่อนเปิด Versioning'))
add(P('ถ้าต้องการกู้คืนไฟล์เวอร์ชันเก่า ให้ติ๊กเลือกเวอร์ชันนั้นแล้ว **Download** หรือ **Open** ได้'))
add(IMG(photo('59'), 'รูปที่ 10.34 ไฟล์มี 2 เวอร์ชัน'))
add(BOX('**ข้อควรรู้เรื่อง Versioning:** เปิดแล้ว**ปิดกลับไม่ได้** ทำได้แค่ Suspend (หยุดสร้างเวอร์ชันใหม่แต่เก็บเวอร์ชันเดิมไว้) '
        'ทุกเวอร์ชันคิดค่าพื้นที่แยกกัน และการ Delete ไฟล์ตามปกติจะแค่ใส่ Delete marker ไฟล์เดิมยังอยู่ '
        'ถ้าต้องการลบจริงต้องเปิด Show versions แล้วลบทีละเวอร์ชัน หรือใช้ Empty bucket'))
add(SUB('ส่วน G: คืนทรัพยากร (Clean up)'))
add(STEP('10.35', 'ลบ bucket **test555test** ด้วยวิธีเดียวกับขั้นตอนที่ 10.23–10.26 (**Empty** ก่อนแล้วจึง **Delete**) '
                  'Empty bucket จะลบทุกเวอร์ชันของทุก object ให้ด้วย', keep_next=False))

# ---------- Summary ----------
add(H('สรุป Part 3'))
add(SUB('ค่าที่ใช้ในแลปนี้ (ใช้อ้างอิงเมื่อทำซ้ำ)'))
add(TABLE(['รายการ', 'ค่าที่ใช้', 'หมายเหตุ'],
          [['Instance', 'volumeLab (i-0b9956a1e952c5487)', 'Windows Server 2025, m7i-flex.large, us-east-1d'],
           ['Root volume', 'vol-08555b4460a8d5a77', '30 GiB gp3, /dev/sda1 (ไดรฟ์ C:)'],
           ['Data volume', 'vol-01f3205f5c3e2ddaa', 'gp3 100 GiB → 150 GiB, us-east-1d, xvdb'],
           ['ไดรฟ์ใน Windows', 'D: 99.98 GB, E: 50 GB', 'E: มาจากพื้นที่ที่ขยายเพิ่ม'],
           ['Snapshot', 'snap-006e27c18b8c4b275', 'Description TestSnapshot, Volume size 150 GiB'],
           ['Volume จาก Snapshot', 'vol-058841f3897d8a266', '150 GiB gp3, us-east-1a'],
           ['Bucket แรก', 'test9452test', 'us-east-1, General purpose, ลบแล้ว'],
           ['ไฟล์ทดสอบ', 'SA Project Note.txt', '679 B, Storage class Standard'],
           ['Object URL', 'https://test9452test.s3.us-east-1.amazonaws.com/SA+Project+Note.txt', 'ต้องให้ Everyone Read ก่อนจึงเปิดได้'],
           ['สิทธิ์สาธารณะ', 'Bucket: Everyone List / Object: Everyone Read', 'ปิด Block all public access, ACLs enabled, Bucket owner preferred'],
           ['Folder', 'testFolder/', 'คัดลอก SA Project Note.txt เข้าไป'],
           ['Bucket ที่สอง', 'test555test', 'Bucket Versioning: Enabled, มี 2 เวอร์ชัน']],
          [2400, 3200, 3400]))
add(SUB('สิ่งที่ควรจำจาก Part 3'))
add(BUL('EBS volume อยู่ใน AZ เดียว และ Attach ได้เฉพาะกับ instance ใน AZ เดียวกัน'))
add(BUL('volume ใหม่ที่ Attach แล้วต้องสร้าง partition ใน Disk Management (New Simple Volume) ก่อน Windows จึงจะใช้งานได้'))
add(BUL('Modify volume ขยายขนาดได้ขณะเครื่องเปิดอยู่ แต่ลดขนาดไม่ได้ และต้องจัดการพื้นที่ใหม่ใน Windows เอง (New Simple Volume หรือ Extend Volume)'))
add(BUL('ข้อมูลใน EBS ไม่หายเมื่อ Detach และนำไป Attach กับเครื่องอื่นได้'))
add(BUL('Snapshot ใช้สำรองข้อมูลและสร้าง volume ใหม่ได้ใน AZ ใดก็ได้ของ Region เดียวกัน ขนาด volume ใหม่ต้องไม่น้อยกว่า Snapshot'))
add(BUL('volume ที่สร้างเพิ่มและ Snapshot ไม่ถูกลบตอน Terminate instance ต้องลบเองเสมอ'))
add(BUL('EBS เป็นดิสก์ที่ต้องต่อกับ EC2 ส่วน S3 เป็นที่เก็บไฟล์ที่เข้าถึงผ่าน URL ได้โดยตรงโดยไม่ต้องมีเครื่อง'))
add(BUL('ชื่อ bucket ต้องไม่ซ้ำกับใครในโลก และ bucket กับ object เป็น private เป็นค่าเริ่มต้น'))
add(BUL('การเปิดไฟล์ให้สาธารณะอ่านได้ต้องทำ 3 ขั้น: ปิด Block public access → เปิด ACLs enabled → ให้ Everyone Read ที่ object'))
add(BUL('ลบ bucket ที่ยังมี object ไม่ได้ ต้อง Empty bucket ก่อน'))
add(BUL('Bucket Versioning เก็บทุกเวอร์ชันเมื่ออัปโหลดไฟล์ชื่อเดิมทับ เปิดแล้วปิดกลับไม่ได้ ทำได้แค่ Suspend'))
add(PAGEBREAK())

splice_part(UN, 3, ''.join(X), IMG)
