from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles

SQLALCHEMY_DATABASE_URL = "sqlite:///./toplanti_veritabani.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

class ToplantiModel(Base):
    __tablename__ = "toplantilar"

    id = Column(Integer, primary_key=True, index=True)
    konu = Column(String, index=True)
    tarih = Column(DateTime)
    baslangic_saati = Column(String)
    bitis_saati = Column(String)
    katilimcilar = Column(String)

Base.metadata.create_all(bind=engine)

uygulama = FastAPI()

uygulama.mount("/static", StaticFiles(directory="static"), name="index.html")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Toplanti(BaseModel):
    konu: str
    tarih: str
    baslangic_saati: str
    bitis_saati: str
    katilimcilar: List[str]

@uygulama.post("/toplanti/")
async def toplanti_ekle(toplanti: Toplanti):
    db = next(get_db())
    db_toplanti = ToplantiModel(
        konu=toplanti.konu,
        tarih=datetime.strptime(toplanti.tarih, "%Y-%m-%d"),
        baslangic_saati=toplanti.baslangic_saati,
        bitis_saati=toplanti.bitis_saati,
        katilimcilar=",".join(toplanti.katilimcilar)
    )
    db.add(db_toplanti)
    db.commit()
    db.refresh(db_toplanti)
    return {"mesaj": "Toplanti başarıyla eklendi", "toplanti": db_toplanti}

@uygulama.get("/toplanti/")
async def toplantilari_listele():
    db = next(get_db())
    toplantilar = db.query(ToplantiModel).all()
    return toplantilar

@uygulama.put("/toplanti/{toplanti_id}")
async def toplanti_guncelle(toplanti_id: int, toplanti: Toplanti):
    db = next(get_db())
    db_toplanti = db.query(ToplantiModel).filter(ToplantiModel.id == toplanti_id).first()
    if db_toplanti is None:
        raise HTTPException(status_code=404, detail="Toplanti bulunamadı")
    db_toplanti.konu = toplanti.konu
    db_toplanti.tarih = datetime.strptime(toplanti.tarih, "%Y-%m-%d")
    db_toplanti.baslangic_saati = toplanti.baslangic_saati
    db_toplanti.bitis_saati = toplanti.bitis_saati
    db_toplanti.katilimcilar = ",".join(toplanti.katilimcilar)
    db.commit()
    return {"mesaj": "Toplanti başarıyla güncellendi", "toplanti": db_toplanti}

@uygulama.delete("/toplanti/{toplanti_id}")
async def toplanti_sil(toplanti_id: int):
    db = next(get_db())
    db_toplanti = db.query(ToplantiModel).filter(ToplantiModel.id == toplanti_id).first()
    if db_toplanti is None:
        raise HTTPException(status_code=404, detail="Toplanti bulunamadı")
    db.delete(db_toplanti)
    db.commit()
    return {"mesaj": "Toplanti başarıyla silindi", "toplanti": db_toplanti}
