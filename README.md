# Toplantı Yönetim Uygulaması

Bu uygulama, toplantıların oluşturulmasını, güncellenmesini, listelenmesini ve silinmesini sağlayan bir API sunar. Toplantılar için konu, tarih, başlangıç saati, bitiş saati ve katılımcılar gibi bilgileri yönetebilirsiniz.

## Kurulum

Projeyi klonlayın:

   ```bash
   git clone https://github.com/Ldreen/Toplant-.git

   cd Toplantı
```
## Kullanım
Uygulamayı başlatmak için:

```bash
uvicorn webService:uygulama --reload
```
Daha sonra http://localhost:8000/docs adresine giderek API belgelerini görebilir ve API'yi test edebilirsiniz.

##### Arayüz için  http://127.0.0.1:8000/static/index.html adresini gidebilirsiniz.

## API Endpoints
#### POST /toplanti/: Yeni bir toplantı ekler.
#### GET /toplanti/: Tüm toplantıları listeler.
#### PUT /toplanti/{toplanti_id}: Belirli bir toplantıyı günceller. 
#### DELETE /toplanti/{toplanti_id}: Belirli bir toplantıyı siler.

## Teknolojiler
#### FastAPI: Hızlı ve modern API geliştirmek için kullanılan Python web çerçevesi.
#### SQLAlchemy: SQL veritabanı işlemleri için kullanılan ORM (Object-Relational Mapping) kütüphanesi.
