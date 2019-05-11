# https://vef-2019-v.herokuapp.com/

# Lokaverkefni
Stutt samantekt um verkefnið:

    Til að geta séð innihald vefsíðunnar þarf notandi að vera til í gagnagrunni.
    Ef notandi er ekki í session er hann færður í nýskráningu.
    Þegar að notandi er skráður inn getur hann séð færslur frá öðrum notendum.
    Notandi getur sett inn færslu og einnig eytt þeim úr gagnagrunni, valmöguleiki um að eyða færslum birtist við færslur sem notandi hefur sett inn á síðuna.
    Færslurnar innihalda Titil, mynd og innihaldslýsingu.
    Í gagnagrunninum eru tvær töflur, grein og notendur.
    Báðar innihalda userid og heldur síðan þannig utan um hvaða notandi á hvaða færslu.
  
Útlit:

    Vefsíðan er ekkert sérlega falleg, enda svolítið langt síðan að ég hef þurft að nota CSS af einhverju viti og er því nokkuð ryðgaður.
    Header er á síðunni sem býður notanda flýtileiðir til að búa til færslu eða skrá sig út.
    Einnig er headerinn með flýtileiðir á miðannarverkefnið og verkefni 7.
  
Bakendinn:

    Öll gagnagrunnsvinnsla er unnin með PostgreSQL í gegnum gagnagrunn frá Heroku.
    Þetta er fyrsti Python áfanginn minn og er ég því ekki með góðan grunn í Python, þar af leiðandi er app.py fullt af spagettí kóða. Hefði líklegast getað sleppt því að skrifa út gagnagrunnsvinnsluna í hverju einasta falli og sett það í function sem ég myndi kalla á.
    Er einnig frekar ryðgaður í SQL og gat því ekki birt nafn gefins notanda við hverja færslu, einungis ID, reyndi að fikta með JOIN en það spýtti bara út einhverjum villukóðum.
