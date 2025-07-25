import requests
from bs4 import BeautifulSoup as BS

from data import db_session
from data.oly import Oly


class Parser:
    def __init__(self, subject, clas, period):
        r = requests.get(
            f'https://olimpiada.ru/activities?subject%{subject}=on&class={clas}&type=any&period_date=&period={period}')
        html = BS(r.content, 'html.parser')
        self.html = html

    def additional_information(self, obj):
        el_link = obj.select('.new_link')[0]
        el_date = obj.select('.grey')[0]
        try:
            el_materials = obj.select('.prepare_steps .color')[0].get('href')
        except IndexError:
            el_materials = ''
        return ' '.join(el_date.text.split('\n')[-2:]).replace('\xa0', ''), (
            el_link.text.replace('\t', '').replace('\n', ' '),
            el_link.get('href')), el_materials

    def oly(self, i):
        html = self.html
        db_sess = db_session.create_session()
        olymps = db_sess.query(Oly).all()

        el = html.select('.olimpiada.fav_olimp ')[i]
        title = el.select('.headline')[0].text
        for oly in olymps:
            if oly.name == title:
                return oly
        rate = el.select('.pl_rating')[0].text
        link = el.select('.none_a')[0].get('href')
        oly_page = requests.get(f'https://olimpiada.ru{link}')
        oly_html = BS(oly_page.content, 'html.parser')
        start, last_news, materials_link = self.additional_information(oly_html)
        new_oly = Oly(name=title,
                      link=link,
                      start=start,
                      rate=rate,
                      last_news=last_news[0],
                      materials_link=materials_link)

        db_sess.add(new_oly)
        db_sess.commit()
        return db_sess.query(Oly).filter(Oly.name == title).first()





if __name__ == "__main__":
    db_session.global_init("db/oly0.db")
    db_sess = db_session.create_session()
    a = Parser('5B6%5D', '10', 'year')
    for i in range(5):
        print(a.oly(i).last_news)
