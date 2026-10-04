# PLAN-ROUTE | v2.0 | from SPEC-ROUTE v2.0 (B1 - กลุ่ม 2)

## 1. สรุปแนวทาง
- ฟีเจอร์นี้ให้ซาเล้งเห็นรายการผู้ขายภายในรัศมี 5 กม. และรับงานตามตำแหน่งและช่วงเวลาที่ตกลงกันได้โดยไม่ต้องเรียกคนกลางหรือมีการโทรถามซ้ำ
- ภาพรวมของระบบจะมี 3 ชั้นหลัก: ค้นหา/กรองรายการตามพิกัด, ตรวจสอบสิทธิ์และการรับงานพร้อมกัน, และแสดง/ซ่อนข้อมูลผู้ขายตามความเป็นส่วนตัว
- ส่วนสำคัญที่ต้องป้องกันคือปัญหาการกดรับงานพร้อมกัน (BR-02), ความถูกต้องของ GPS และความเร็วของการค้นหา, และการยืนยันตัวตนผ่าน API ภายนอก
- ความสำคัญของ plan นี้คือยึดความต้องการจาก REQ-FN-002, REQ-BR-002, REQ-QA-002 และ REQ-SEC-002 โดยไม่ข้าม Open Questions ที่ยังเปิดอยู่
- งานจะเริ่มจากการกำหนด domain model, API contract, และ test cases จาก AC-04-01 ถึง AC-04-08 ก่อนพัฒนา GUI และ integration กับ Maps/GPS/Thai-ID/DBD API

## 2. เทคโนโลยีที่ใช้
| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| Python FastAPI + PostgreSQL + React (Vite) | รอทีมเลือก / ไม่ได้มาจาก spec | ชุดแนะนำ 1: เหมาะกับ API แบบ REST + user-facing web และทดสอบด้วย pytest + Vitest |
| Node.js + Express + PostgreSQL + React | รอทีมเลือก / ไม่ได้มาจาก spec | ชุดแนะนำ 2: เหมาะถ้า team มีความคุ้นเคยกับ JavaScript และรองรับธุรกิจที่ต้องจัดการ API จาก frontend เดียวกัน |
| Django + DRF + PostgreSQL + React | รอทีมเลือก / ไม่ได้มาจาก spec | ชุดแนะนำ 3: เหมาะถ้าต้องการโครงสร้างแบบ full-stack ที่มี validation และ admin อย่างครบถ้วน |

- โครงสร้างเริ่มต้นที่ควรใช้หลังทีมเลือกเป็น 1 ใน 3 ชุดข้างต้น: `backend/app/`, `backend/tests/`, `frontend/src/`, `backend/requirements.txt` หรือ `package.json` ตาม stack ที่เลือก, และ `pytest.ini` หรือ `vitest.config.*` สำหรับรัน test
- โครงงานปัจจุบันยังไม่มีโค้ดตัวจริงใน repo ดังนั้นฟิลด์ dependency ที่ควรมีคือ API framework, ORM/DB driver, validation library, และ React/Vite สำหรับ UI
- คำสั่งรัน test ที่ควรใช้ภายหลังทีมเลือก stack: `cd backend && pytest -q` และ `cd frontend && npm test` (หรือ `npm run test -- --run`) เพื่อให้สอดคล้องกับ task T-01/T-02/T-03 ตาม AC-04
- การตัดสินใจเรื่องภาษา/framework ต้องรอการยืนยันจากทีม เพราะ spec ไม่มีบันทึกที่ระบุ stack อย่างเป็นทางการ

## 3. โมเดลข้อมูล
| Entity | ฟิลด์หลัก | รองรับ FR/AC |
|---|---|---|
| ScrapRequest | id, sellerId, geoPoint, scrapType, estimatedPrice, status, createdAt, acceptedBySalengId, acceptedAt, expiresAt | REQ-FN-002, REQ-FN-001, REQ-BR-002, AC-04-01..08 |
| SalengProfile | id, thaiIdVerified, dbdIdVerified, lastLocationLat, lastLocationLng, lastLocationUpdatedAt | SC-04, REQ-FN-002 |
| SellerProfile | id, userType, serviceAddressGeoPoint, addressVisible, consentToShareLocation | REQ-SEC-002 |
| RouteMatch | requestId, salengId, distanceKm, matchedAt | REQ-FN-002, REQ-QA-002 |
| VerificationAttempt | id, salengId, provider, status, timestamp, errorCode | SC-04 |
| PriceReference | scrapType, date, basePriceMin, basePriceMax, unit | REQ-FN-001 |

- ไม่มีการเก็บเลขประจำตัวประชาชนแบบ raw ใน model เนื่องจาก spec ระบุว่า `Customer.phone PII` และ `ServiceAddress.geoPoint PII` เท่านั้น และชื่อฐานข้อมูลที่ยืนยันตัวตนจะผ่าน API ภายนอกแทนการเก็บข้อมูลทางตรงใน schema ส่วนใหญ่
- GeoPoint เท่านั้นที่ใช้เป็นพิกัดสำหรับ filtering แบบรัศมี ไม่บันทึกเลขที่บ้านแบบละเอียดซึ่งเป็นสิ่งที่ต้องซ่อนจนกว่าจะมีการยอมรับงาน

## 4. API / หน้าจอ
| Method / Path | Input หลัก | Output หลัก | รองรับ FR |
|---|---|---|---|
| GET /api/requests/nearby | salengLat, salengLng, radiusKm=5, scrapType?, timeWindow | รายการ ScrapRequest ที่อยู่ในรัศมีและยังว่าง | REQ-FN-002, AC-04-01, AC-04-02 |
| GET /api/requests/{id} | requestId | รายละเอียด request, ราคา, ประเภทขยะ, สถานะ | REQ-FN-001, AC-04-04 |
| POST /api/requests/{id}/accept | salengId, requestId, lat, lng, timestamp | ผลสำเร็จ/ปฏิเสธพร้อม status ใหม่ | REQ-BR-002, AC-04-05 |
| POST /api/salengs/verify | thaiId, dbdId, salengId | success/fail + provider reference | SC-04 |
| GET /api/salengs/me/location | salengId | พิกัดปัจจุบันและความถูกต้องของ GPS | REQ-OP-002, AC-04-06 |
| GET /api/requests?sort=distance | query params | รายการที่เรียงลำดับตามระยะทาง | REQ-QA-002, AC-04-07 |
| UI: หน้าแสดงเส้นทาง/รายการรอรับงาน | ซาเล้ง login + GPS enable | รายการผู้ขายที่ใกล้ที่สุดในรัศมี 5 กม. | REQ-FN-002, REQ-QA-002 |
| UI: หน้ารายละเอียดการรับงาน | requestId | ราคากลาง + ข้อมูลจำเป็น + ปุ่มรับงาน | REQ-FN-001, REQ-SEC-002 |

## 5. ตารางตรวจ Constraints
| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| REQ-CON-002 | ใช้ในการออกแบบ rate-limit/ quota สำหรับ Maps/GPS API request และ fallback เมื่อเกินโควต้า | ใช้แล้ว |
| REQ-CON-003 | ยังไม่ถูกใช้ใน design เนื่องจาก spec ระบุแค่ข้อจำกัดน้ำหนักบรรทุกของยานพาหนะ แต่ฟีเจอร์นี้เป็นการค้นหาและรับงานตามเส้นทาง ไม่ได้มี workflow ที่ต้องคำนึงถึงภาระบรรทุกโดยตรง | ยังไม่ได้ใช้ เพราะ... |
| SC-04 | เชื่อมกับ flow การยืนยันตัวตนซาเล้งและผู้ขายผ่าน Thai-ID / DBD-ID | ใช้แล้ว |

## 6. แผนทดสอบจาก Acceptance Criteria
| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-04-01 | `test_AC_04_01_search_by_radius` | ตรวจว่า API คืนเฉพาะผู้ขายที่อยู่ภายในรัศมี 5 กม. จากตำแหน่งซาเล้ง |
| AC-04-02 | `test_AC_04_02_route_list_orders_by_distance` | ตรวจว่า list แสดงเรียงจากใกล้สุดไปไกลสุด และ filter ตาม distance |
| AC-04-03 | `test_AC_04_03_empty_result_when_out_of_radius` | ตรวจว่าถ้าห่างเกิน 5 กม. ไม่มีรายการแสดง |
| AC-04-04 | `test_AC_04_04_show_price_reference` | ตรวจว่ารายการมีประเภทขยะและราคากลางอ้างอิงตามวันที่เลือก |
| AC-04-05 | `test_AC_04_05_single_accept_per_request` | ตรวจว่ามีเพียงซาเล้งคนเดียวที่สามารถ accept request ได้ และคนถัดไปต้องเห็น status เผื่อรับแล้ว |
| AC-04-06 | `test_AC_04_06_gps_accuracy_threshold` | ตรวจว่าค่าความคลาดเคลื่อน GPS อยู่ในเกณฑ์ <= 15% เหนือค่าที่ใช้เปรียบเทียบ |
| AC-04-07 | `test_AC_04_07_response_time_under_3s` | ทำ performance test แบบ p95 หรือ load basic สำหรับ nearby list และยืนยันเวลาไม่เกิน 3 วินาที |
| AC-04-08 | `test_AC_04_08_hidden_address_until_acceptance` | ตรวจว่าพิกัดบ้านเลขที่ผู้ขายถูกซ่อนไว้จนกว่าจะมีการ accept และเปิดเผยได้เฉพาะหลังการรับงาน |

## 7. ลำดับงาน
1. กำหนด model, status, และ validation สำหรับ ScrapRequest และ SellerProfile (รองรับ REQ-FN-002, REQ-SEC-002, REQ-BR-002)
2. สร้าง API ค้นหา/กรอง nearby list และรายละเอียด request พร้อม pagination/limit (รองรับ REQ-FN-002, REQ-FN-001, AC-04-01..04)
3. สร้าง flow ยืนยันตัวตนซาเล้งและผู้ขายผ่าน Thai-ID/DBD-ID ก่อนเปิดสิทธิ์รับงาน (รองรับ SC-04)
4. พัฒนา logic accept request แบบ single-accept + concurrency lock (รองรับ REQ-BR-002, Q-01, AC-04-05)
5. วัด GPS accuracy และ response time เพื่อให้ตรงกับ REQ-OP-002, REQ-QA-002, AC-04-06, AC-04-07
6. สร้าง UI ห้องค้นหา/รายละเอียด/รับงาน พร้อมซ่อนพิกัดจนกว่ากดรับแล้ว (รองรับ REQ-SEC-002, AC-04-08)
7. ทำ regression test ครบทุก AC และบันทึกผลการทดสอบที่เกี่ยวกับ Open Questions ที่ยังเปิดไว้

## 8. สิ่งที่ยังไม่ทำ
- Q-01: กรณีซาเล้ง 2 คนกดรับงานพร้อมกันในเสี้ยววินาทีเดียวกัน — ส่วนที่เกี่ยวข้องกับข้อนี้จะยังไม่สร้างจนกว่าจะได้คำตอบว่าใช้ “request ถึง server ก่อน” หรือ “timestamp ของ user action” เป็นเกณฑ์หลัก
- Q-02: ระยะทาง “5 กม.” ควรใช้วิธีคำนวณแบบใด (ระยะทางเส้นตรง vs ระยะทางตามทาง) — ส่วนที่เกี่ยวข้องกับข้อนี้จะยังไม่สร้างจนกว่าจะได้คำตอบและระบุใน requirement ของ API
- Q-03: การยืนยันตัวตนผ่าน Thai-ID / DBD-ID มี handling อย่างไรเมื่อล้ม/timeout/ปฏิเสธ — ส่วนที่เกี่ยวข้องจะยังไม่สร้างจนกว่าจะได้คำตอบว่าต้อง reject หรือ retry หรือ retry with backoff
- Q-04: หากไม่ระบุ stack เทคโนโลยีอย่างชัดเจน ทีมต้องเลือก 1 ชุดก่อนเริ่มพัฒนา actual implementation เพราะ current plan อยู่ในระดับ candidate only

## หมายเหตุสำหรับทีม
- ความถูกต้องทางธุรกิจที่ยังมีความไม่แน่ชัดคือวิธีคำนวณระยะทางและกฎ concurrent accept จึงต้องมีการยืนยันก่อนเริ่มเขียนโค้ดจริง
- แต่ละแผนส่วนด้าน API, data model, test และ UI 都มี traceability ไปยัง requirement และ acceptance criteria ที่ระบุใน spec แล้ว
- หากต้องการให้ plan นี้เป็น “final” ต้องยืนยัน stack เทคโนโลยีและคำตอบ Q-01 ก่อน เพราะตอนนี้ยังเป็น draft ที่เปิดให้ team ตัดสินใจต่อไป
