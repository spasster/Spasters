import requests
from enum import Enum


class DocumentType(Enum):
    # Паспорт гражданина СССР
    passport_ussr = "01"
    # Свидетельство о рождении
    birth_certificate = "03"
    # Паспорт иностранного гражданина
    passport_foreign = "10"
    # Вид на жительство в России
    residence_permit = "12"
    # Разрешение на временное проживание в России
    residence_permit_temp = "15"
    # Свидетельство о предоставлении временного убежища на территории России
    asylum_certificate_temp = "19"
    # Паспорт гражданина России
    passport_russia = "21"
    # Свидетельство о рождении, выданное уполномоченным органом иностранного государства
    birth_certificate_foreign = "23"
    # Вид на жительство иностранного гражданина
    residence_permit_foreign = "62"


def suggest_inn(surname, name, patronymic, birthdate, doctype, docnumber, docdate):
    url = "https://service.nalog.ru/inn-proc.do"
    data = {
        "fam": surname,
        "nam": name,
        "otch": patronymic,
        "bdate": birthdate,
        "bplace": "",
        "doctype": doctype,
        "docno": docnumber,
        "docdt": docdate,
        "c": "innMy",
        "captcha": "",
        "captchaToken": "",
    }
    resp = requests.post(url=url, data=data)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    response = suggest_inn(
        surname="Нелин",
        name="Данила",
        patronymic="Андреевич",
        birthdate="19.03.2008",
        doctype=DocumentType.passport_russia.value,
        docnumber="61 21 256877",
        docdate="04.04.2022",
    )
    print(response)