# TASKS-ROUTE | v2.0 | from SPEC-ROUTE v2.0 + PLAN-ROUTE v2.0

- Feature: การรับงานตามเส้นทาง (ซาเล้ง)
- Spec ID: SPEC-ROUTE v2.0
- อ้างอิง plan.md: PLAN-ROUTE v2.0
- วันที่: 2026-10-04

สรุป:
- ทำทั้งหมด 10 task
- มี 4 task ที่ต้องรอ Open Questions (Q-01, Q-02, Q-03)

## รายการ task

### T-01 ตั้งโครงโปรเจกต์พื้นฐาน backend/frontend
- รองรับ: REQ-FN-002, REQ-QA-002
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: backend/app/, backend/tests/, frontend/src/, backend/requirements.txt หรือ package manager ตาม plan.md ข้อ 2, frontend/package.json, pytest.ini หรือ vitest.config.*
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: โครงโปรเจกต์เริ่มต้นรัน test เปล่าผ่าน 1 ตัว
- สถานะ: พร้อมทำ

### T-02 สร้างโมเดลข้อมูลสำหรับคำขอและผู้ขาย
- รองรับ: REQ-FN-002, REQ-FN-001, REQ-SEC-002
- ตรวจด้วย: AC-04-04, AC-04-08
- ไฟล์ที่แตะ: backend/app/db/models.py, backend/app/db/migrations/*.py, backend/app/config.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: schema สำหรับ ScrapRequest, SellerProfile และ PriceReference โหลดได้และผ่าน test schema ฐานข้อมูลเบื้องต้น
- สถานะ: เสร็จ รอทีมตรวจ

### T-03 ค้นหารายการใกล้ที่สุดตามรัศมี 5 กม.
- รองรับ: REQ-FN-002, REQ-QA-002
- ตรวจด้วย: AC-04-01, AC-04-02, AC-04-03, AC-04-07
- ไฟล์ที่แตะ: backend/app/requests/service.py, backend/app/requests/router.py, backend/app/api/client.py, frontend/src/pages/RouteList.jsx
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: API nearby คืนเฉพาะรายการที่อยู่ภายในรัศมี 5 กม. และแสดงเรียงจากใกล้สุดก่อนตามลำดับที่กำหนด
- สถานะ: รอ Q-02

### T-04 สร้าง flow ยืนยันตัวตนซาเล้งและผู้ขาย
- รองรับ: SC-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-04
- ไฟล์ที่แตะ: backend/app/verification/service.py, backend/app/verification/router.py, backend/app/verification/provider.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: flow ตรวจสถานะการยืนยันตัวตนผ่าน Thai-ID/DBD-ID บันทึกผล success/fail และป้องกันการเข้าใช้งานก่อนยืนยันสำเร็จ
- สถานะ: รอ Q-03

### T-05 สร้าง logic รับงานแบบ single-accept และป้องกันซ้ำ
- รองรับ: REQ-BR-002
- ตรวจด้วย: AC-04-05
- ไฟล์ที่แตะ: backend/app/requests/accept.py, backend/app/requests/router.py, backend/tests/test_route_accept.py
- ต้องทำหลัง: T-03, T-04
- เสร็จเมื่อ: test_AC_04_05_single_accept_per_request ผ่านและการรับงานซ้ำถูกปฏิเสธด้วยสถานะที่ชัดเจน
- สถานะ: รอ Q-01

### T-06 วัดความถูกต้อง GPS และเวลา response
- รองรับ: REQ-OP-002, REQ-QA-002
- ตรวจด้วย: AC-04-06, AC-04-07
- ไฟล์ที่แตะ: backend/app/geo/service.py, backend/tests/test_route_accuracy.py, frontend/src/pages/RouteList.jsx
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: test_AC_04_06_gps_accuracy_threshold และ test_AC_04_07_response_time_under_3s ผ่านในสภาพทดสอบที่กำหนด
- สถานะ: รอ Q-02

### T-07 สร้างหน้าแสดงรายการและรายละเอียดรับงานแบบ mock API
- รองรับ: REQ-FN-002, REQ-FN-001, REQ-SEC-002
- ตรวจด้วย: AC-04-02, AC-04-04, AC-04-08
- ไฟล์ที่แตะ: frontend/src/pages/RouteList.jsx, frontend/src/pages/RouteDetail.jsx, frontend/src/api/client.js, frontend/src/__tests__/route-ui.test.jsx
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้ารายการแสดงใกล้สุด/ราคากลาง/ปุ่มรับงาน และพิกัดบ้านเลขที่ถูกซ่อนจนกว่าจะรับงานสำเร็จ
- สถานะ: พร้อมทำ

### T-08 ต่อเชื่อม frontend กับ API จริงและตรวจ regression
- รองรับ: REQ-FN-002, REQ-QA-002
- ตรวจด้วย: AC-04-02, AC-04-07
- ไฟล์ที่แตะ: frontend/src/api/client.js, frontend/src/pages/RouteList.jsx, frontend/src/pages/RouteDetail.jsx, frontend/src/setupTests.js
- ต้องทำหลัง: T-03, T-07
- เสร็จเมื่อ: หน้า UI ใช้ API จริงและไม่ล้มเมื่อส่ง request/response จาก backend พร้อม test UI regression ผ่าน
- สถานะ: พร้อมทำ

### T-09 สร้างชุดทดสอบรวมสำหรับทุก AC-04
- รองรับ: REQ-FN-002, REQ-FN-001, REQ-BR-002, REQ-OP-002, REQ-QA-002, REQ-SEC-002
- ตรวจด้วย: AC-04-01, AC-04-02, AC-04-03, AC-04-04, AC-04-05, AC-04-06, AC-04-07, AC-04-08
- ไฟล์ที่แตะ: backend/tests/, frontend/src/__tests__/
- ต้องทำหลัง: T-03, T-05, T-06, T-07, T-08
- เสร็จเมื่อ: ทุก AC-04-01 ถึง AC-04-08 มี test ครอบคลุมอย่างน้อย 1 ตัว และผ่านตามกติกาของ feature
- สถานะ: พร้อมทำ

### T-10 ตรวจสอบข้อจำกัดน้ำหนักยานพาหนะก่อนรับงาน
- รองรับ: REQ-CON-003
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-10
- ไฟล์ที่แตะ: backend/app/requests/vehicle_constraints.py, backend/app/requests/router.py
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: ระบบปฏิเสธหรือแสดง warning เมื่อยานพาหนะซาเล้งเกินข้อจำกัดน้ำหนักก่อนเริ่มรับงาน
- สถานะ: พร้อมทำ

## ตารางตรวจความครบ (AC -> task)
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-04-01 | T-03, T-09 |
| AC-04-02 | T-03, T-07, T-08, T-09 |
| AC-04-03 | T-03, T-09 |
| AC-04-04 | T-02, T-07, T-09 |
| AC-04-05 | T-05, T-09 |
| AC-04-06 | T-06, T-09 |
| AC-04-07 | T-03, T-06, T-08, T-09 |
| AC-04-08 | T-02, T-07, T-09 |

## ตารางตรวจความครบ (Constraint -> task)
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| REQ-CON-002 | T-03, T-06, T-08 |
| REQ-CON-003 | T-10 |

## สิ่งที่ยังไม่ทำ
- Q-01: กรณีซาเล้ง 2 คนกดรับงานพร้อมกันในเสี้ยววินาทีเดียวกัน — task ที่เกี่ยวข้อง: T-05; จะเริ่มสร้างเมื่อได้รับคำตอบว่ากำหนดสิทธิ์ด้วย “request ถึง server ก่อน” หรือ “timestamp ของ user action”
- Q-02: ระยะทาง “5 กม.” ควรใช้วิธีคำนวณแบบใด (ระยะทางเส้นตรง vs ระยะทางตามทาง) — task ที่เกี่ยวข้อง: T-03, T-06; จะเริ่มสร้างเมื่อทีมกำหนดกฎคำนวณก่อน
- Q-03: การยืนยันตัวตนผ่าน Thai-ID / DBD-ID มี handling อย่างไรเมื่อล้ม/timeout/ปฏิเสธ — task ที่เกี่ยวข้อง: T-04; จะเริ่มสร้างเมื่อทีมกำหนดว่าจะ reject หรือ retry หรือ retry with backoff

