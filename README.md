# گزارش پروژه پایانی درس پایگاه داده پیشرفته


**دانشجو:** محمد امین بشارتیان
**درس:** پایگاه داده پیشرفته
**استاد:** دکتر آرمین رشنو
**نیمسال:** پاییز ۱۴۰۴

## معرفی پروژه

در این پروژه، یک وب‌سرویس مبتنی بر FastAPI طراحی و پیاده‌سازی شده است که عملیات مرتبط با پایگاه داده را به‌صورت API در بستر وب ارائه می‌دهد. هدف پروژه، آشنایی عملی با استقرار سرویس، مدیریت دامنه، SSL، GitHub و CI/CD مطابق مراحل تعریف‌شده در پروژه پایانی درس می‌باشد.

## مرحله ۱

از طریق محیط Swagger همه API های سمت سرور بررسی شده و هر کدام تست شوند. در گام اول
لیست همه API ها در یک جدول شامل نام، ورودی، خروجی و ... مستند سازی شود.


| Http Request |       Name        |         Path         |                                                             Query                                                              |                                                                                      Request Body                                                                                      |                                                                                                                                                                                                                                          Output                                                                                                                                                                                                                                          |
| :----------: | :---------------: | :------------------: | :----------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|     POST     | Admin Create User |          ""          |                                                               ""                                                               | <br>  "username": "string",<br>  "password": "string",<br>  "Fullname": "string",<br>  "email": "string",<br>  "disabled": false,<br>  "role_id": 0,<br>  "phone_number": "string"<br> |                                                                                                                                                                                                                                         "string"                                                                                                                                                                                                                                         |
|     GET      |     Get User      |  "user_id": integer  |                                                               ""                                                               |                                                                                           ""                                                                                           |                                                                     <br>  "created_at": "2025-12-21T21:54:00.854Z",<br>  "created_at_jalali": "string",<br>  "updated_at": "2025-12-21T21:54:00.854Z",<br>  "updated_at_jalali": "string",<br>  "id": 0,<br>  "username": "string",<br>  "email": "string",<br>  "fullname": "string",<br>  "phone_number": "string",<br>  "role_id": 0,<br>  "disabled": false<br>                                                                      |
|     PUT      |    Update User    |  "user_id": integer  |                                                               ""                                                               | <br>  "username": "string",<br>  "password": "string",<br>  "fullname": "string",<br>  "email": "string",<br>  "phone_number": "string",<br>  "role_id": 0,<br>  "disabled": true<br>  |                                                                       <br>  "created_at": "2025-12-21T21:55:59.858Z",<br>  "created_at_jalali": "string",<br>  "updated_at": "2025-12-21T21:55:59.858Z",<br>  "updated_at_jalali": "string",<br>  "id": 0,<br>  "username": "string",<br>  "email": "string",<br>  "fullname": "string",<br>  "phone_number": "string",<br>  "role_id": 0,<br>  "disabled": false                                                                        |
|     GET      |   Get All Users   |         <br>         | "page": integer,<br>"size": integer,<br>"sort_by": string \| null,<br>"sort_order": string \| none<br>"search": string \| null |                                                                                                                                                                                        | {<br>  "total": 0,<br>  "size": 0,<br>  "pages": 0,<br>  "items": [<br>    {<br>      "created_at": "2025-12-21T21:57:15.934Z",<br>      "created_at_jalali": "string",<br>      "updated_at": "2025-12-21T21:57:15.934Z",<br>      "updated_at_jalali": "string",<br>      "id": 0,<br>      "username": "string",<br>      "email": "string",<br>      "fullname": "string",<br>      "phone_number": "string",<br>      "role_id": 0,<br>      "disabled": false<br>    }<br>  ]<br>} |
|     POST     |  Create Province  |                      |                                                                                                                                |                                                                          {<br>  "province": "string"<br>}<br>                                                                          |                                                                                                                                                                                                                             {<br>  "province": "string"<br>}                                                                                                                                                                                                                             |
|     GET      | Get All Province  |                      | "page": integer,<br>"size": integer,<br>"sort_by": string \| null,<br>"sort_order": string \| none<br>"search": string \| nul  |                                                                                                                                                                                        |                                                                                                                                                  {<br>  "total": 0,<br>  "size": 0,<br>  "pages": 0,<br>  "items": [<br>    {<br>      "province": "string",<br>      "id": 0,<br>      "created_at": "string"<br>    }<br>  ]<br>}<br>                                                                                                                                                  |
|    DELETE    |  Delete Province  | "province": "string" |                                                                                                                                |                                                                                                                                                                                        |                                                                                                                                                                                                                           {<br>  "message": "string"<br>}<br>                                                                                                                                                                                                                            |
|              |                   |                      |                                                                                                                                |                                                                                                                                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

## مرحله ۲

همه صفحات سمت کاربر بررسی شود و مشخص کنید هر صفحه کدام API را فراخوانی میکند. در این
مرحله تسلط کافی بر تب های مختلف Inspect مرورگر لازم است.

In this step we check the API's requests in each page

### Login Page

After you have entered the username and password:

Inputs:
- username
- password

| Request URL                         | Request Method | Status Code |
| ----------------------------------- | -------------- | ----------- |
| https://edu-api.havirkesht.ir/token | POST           | 200         |

Response:

> {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlZHVfNDAxMTE0MTUwMzYiLCJzY29wZXMiOlsiKiJdLCJyb2xlX2lkIjoxLCJ1c2VyX2lkIjoxMDIyLCJmdWxsbmFtZSI6IlN0dWRlbnQgNDAxMTE0MTUwMzYiLCJleHAiOjE3NjYzNTg0OTgsInRva2VuX3R5cGUiOiJhY2Nlc3MifQ.VJ5VaMTVU3gFqNCQwLdnhtD5nGVM8tAYBhhCn35kuS4",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlZHVfNDAxMTE0MTUwMzYiLCJleHAiOjE3NjY5NTk2OTgsInRva2VuX3R5cGUiOiJyZWZyZXNoIn0.w4vqXTlKNdQtof3SQERU4rv1DOmRn00dBi6822lDUP8",
    "token_type": "bearer"
}


### Dashboard

Query:
- crop_year_id

| Request URL                                                | Request Method | Status Code |
| ---------------------------------------------------------- | -------------- | ----------- |
| https://edu-api.havirkesht.ir/report-full/?crop_year_id=13 | POST           | 200         |

Response:

>{
    "current_contractor_remaining_balance": 3827814550,
    "farmers_commitment_count": 429,
    "total_delivered_tonnage": 16010,
    "total_farmers_debt": 44530209685,
    "total_farmers_receivable": 1221252734,
    "farmers_remaining_settlement": 43308956951,
    "contractor_fee": 669737013,
    "contractor_seed_profit": 0,
    "contractor_pesticide_profit": 0,
    "overall_contractor_status": 3827814550,
    "report_generated_at": "1404/09/30 22:08:24",
    "crop_year_name": "1404"
}

### Placed Farmer Page

Path:
- user_id


| Request URL                              | Request Method | Status Code |
| ---------------------------------------- | -------------- | ----------- |
| https://edu-api.havirkesht.ir/users/1022 | POST           | 200         |

Response:
>{
    "created_at": "2025-11-04T06:15:54.533834Z",
    "created_at_jalali": "1404/08/13 06:15:54",
    "updated_at": "2025-11-04T06:15:54.533834Z",
    "updated_at_jalali": "1404/08/13 06:15:54",
    "id": 1022,
    "username": "edu_40111415036",
    "email": "edu_40111415036@gmail.com",
    "fullname": "Student 40111415036",
    "phone_number": "09181000030",
    "role_id": 1,
    "disabled": false
}


## مرحله ۳

لیست همه جداول، فیلدهای هر جدول و ارتباطات بین جداول در اختیار شما قرار داده می شود. یک پایگاه
داده رابطه ای را پیاده سازی کنید.

```sql
CREATE TABLE province (
    id BIGSERIAL PRIMARY KEY,
    province CHARACTER VARYING NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

```sql
CREATE TABLE city (
    id BIGSERIAL PRIMARY KEY,
    city CHARACTER VARYING NOT NULL,
    province_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT fk_city_province
        FOREIGN KEY (province_id)
        REFERENCES province(id)
        ON DELETE CASCADE
);
```

```sql
CREATE TABLE village (
    id BIGSERIAL PRIMARY KEY,
    village CHARACTER VARYING NOT NULL,
    city_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT fk_village_city
        FOREIGN KEY (city_id)
        REFERENCES city(id)
        ON DELETE CASCADE
);
```

```sql
CREATE TABLE farmer(
	id BIGSERIAL PRIMARY KEY,
	national_id CHARACTER VARYING NOT NULL,
	full_name CHARACTER VARYING NOT NULL,
	father_name CHARACTER VARYING NOT NULL,
	phone_number CHARACTER VARYING NOT NULL,
	sheba_number_1 CHARACTER VARYING NOT NULL,
	sheba_number_2 CHARACTER VARYING NOT NULL,
	card_number CHARACTER VARYING NOT NULL,
	addres CHARACTER VARYING NOT NULL,
	created_at TIMESTAMPTZ DEFAULT NOW()
)

CREATE INDEX ix_national_id ON public.farmer (national_id)
```

```sql
CREATE TABLE measure_unit(
	id BIGSERIAL PRIMARY KEY,
	unit_name CHARACTER VARYING NOT NULL,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	updated_at TIMESTAMPTZ DEFAULT NOW()
)

CREATE INDEX ix_unit_name ON PUBLIC.measure_unit (unit_name)
```

```sql
CREATE TABLE crop_year(
	id BIGSERIAL PRIMARY KEY,
	crop_year_name CHARACTER VARYING NOT NULL,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	updated_at TIMESTAMPTZ DEFAULT NOW()
)

CREATE INDEX ix_crop_year_name ON PUBLIC.crop_year (crop_year_name)
```

```sql
CREATE TABLE payment_reason(
	id BIGSERIAL PRIMARY KEY,
	resason_name CHARACTER VARYING NOT NULL,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	updated_at TIMESTAMPTZ DEFAULT NOW()
)

CREATE INDEX ix_reason_name ON PUBLIC.payment_reason (reason_name)
```


```sql
CREATE TABLE factory(
	id BIGSERIAL PRIMARY KEY,
	factory_name CHARACTER VARYING NOT NULL,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	updated_at TIMESTAMPTZ DEFAULT NOW()
)

CREATE INDEX ix_factory_name ON PUBLIC.factory (factory_name)
```

![third_3](./images/third_2.png)

## مرحله ۵

همه عملیات موجود در پایگاه داده رابطه ای و غیررابطه ای را در قالب یک وب سرویس بصورت API ایجاد
کنید.

شما میتونید این بخش رو در پوشه routers پیدا کنید.


## مرحله ۶

در این مرحله یک دامنه با پسوند `.ir` به نام زیر تهیه شد:

- **Domain:** `aminbesharatian.ir`

سپس:

- یک حساب کاربری در Cloudflare ایجاد شد
- سپس Nameserver های Cloudflare به دامنه منتقل گردید.
- در آخر رکورد های DNS برای اتصال به IP سرور تنظیم شد.


![sixth_1](./images/sixth_1.png)

![sixth_2](./images/sixth_2.png)


## مرحله ۷

یک سرور مجازی لینوکسی را برای بازه کوتاهی اجاره کنید یا از ارایه دهنده سرورهای رایگان مانند لیارا , یا ... استفاده شود.

برای اجرای پروژه، یک سرور لینوکسی (Ubuntu) از ارائه‌دهنده لیارا تهیه شد.

مشخصات کلی:

- سیستم عامل: Ubuntu
- وب سرور: Nginx
- اجرای API با: FastAPI + Uvicorn

## مرحله ۸

از طریق بستر Github یا فایل های سورس پروژه را از IDE به Repository خود Push کنید و بر روی
سرور خود Clone کنید.

![eighth_1](./images/eighth_1.png)

[Github repository](https://github.com/Amin-BSH/amin_final_adb_project)
## مرحله ۹

پروژه را بر روی سرور مستقر کنید، سپس برای دامنه خود گواهی SSL دریافت و نصب نمایید. در نهایت،
اطمینان حاصل کنید که برنامه از طریق HTTPS بهصورت ایمن در دسترس است.

پس از استقرار کامل پروژه، برای دامنه گواهی SSL دریافت و نصب شد.

مراحل انجام شده طبق داکیومنت سایت liara انجام شده است.

 [داکیومنت liara](https://docs.liara.ir/iaas/ubuntu/how-tos/connect-domain/)

## مرحله ۱۰

از طریق بستر CI/CD فرایند اجرا بر روی سرور را خودکار کنید . به این معنی که بعد از اعمال هر تغییری
در لوکال هاست و پوش کردن آن در گیت هاب ، تغییرات همان لحظه بر روی سرور اعمال شود.

در این مرحله فرآیند CI/CD پیاده‌سازی شد به‌طوری که:

- با هربار push جدید به Github
- تغییرات بصورت خودکار اعمال میشوند
- نیاز به Deploy دستی حذف شد.

## مرحله ۱۱

از طریق سایت liara یک API برای دسترسی به مدل gpt-40-mini تهیه شد.

## مرحله ۱۲

گزارشی از جزئیات همه مراحل فوق به همراه عکس هر مرحله آماده کرده و در فایل README.md قرار
دهید.

در این مرحله تمام مراحل انجام شده مستند سازی شدند.

این فایل به‌عنوان گزارش نهایی پروژه جهت ارائه حضوری استفاده خواهد شد.


**پایان**