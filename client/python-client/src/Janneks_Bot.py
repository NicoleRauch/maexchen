from maexchen_bot import MaexchenBot, Nachrichten


class EinfacherBot(MaexchenBot):
    def reagiere_auf_nachricht(self, nachricht, parameter):
        if (nachricht == Nachrichten.NEUE_RUNDE):
            self.vorherigeSpieler = 0
            self.angesagt = [1, 0]
            self.vorherangesagt = [1, 0]

        if (nachricht == Nachrichten.SPIELER_SAGT_AN):
            self.vorherangesagt = self.angesagt
            self.angesagt = self.zerlege_wuerfel_string(parameter[-1])
            self.zaehleSpieler()

        if (nachricht == Nachrichten.DU_BIST_DRAN):
            token = parameter[-1]
            if self.vorherigeSpieler >= 2:
                if self.ist_pasch(self.angesagt) is False:
                    self.differenz_analyse(token)
                else:
                    self.vorherigeSpieler_analyse(token)
            else:
                self.erwartungswert_analyse(token)

        if (nachricht == Nachrichten.GEWUERFELT):
            token = parameter[-1]
            gewuerfelte_augen = self.zerlege_wuerfel_string(parameter[0])
            if self.ist_hoeher(gewuerfelte_augen, self.angesagt):
                self.sage_an(gewuerfelte_augen, token)
            else:
                self.luege(token)

    def zaehleSpieler(self):
        self.vorherigeSpieler += 1

    def differenz_der_würfel(self):
        differenzDerAnsagen = 0
        for moeglicheZehner in range(self.vorherangesagt[0], self.angesagt[0]):
            ausgangseinser = 1
            if moeglicheZehner == self.vorherangesagt:
                ausgangseinser = self.vorherangesagt[1]

            for moeglicherEinser in range(ausgangseinser, 6):
                zuprüfenderWürfel = moeglicheZehner, moeglicherEinser
                if self.ist_pasch(zuprüfenderWürfel):
                    pass
                else:
                    differenzDerAnsagen += 1
        return differenzDerAnsagen

    def luege(self, token):
        gelogenen_augen = self.hoeher_als_angesagt()
        self.sage_an(gelogenen_augen, token)

    def sage_an(self, gewuerfelte_augen, token):
        self.schicke_nachricht(Nachrichten.ANSAGEN, [self.fuege_wuerfel_zusammen(gewuerfelte_augen), token])

    def hoeher_als_angesagt(self):
        if self.ist_pasch(self.angesagt):
            if self.angesagt == [6, 6]:
                return [2, 1]
            else:
                return [wuerfel + 1 for wuerfel in self.angesagt]
        else:
            return [1, 1]

    def erwartungswert_analyse(self, token, erwartungswert_wuerfel=[6, 4]):
        if self.ist_hoeher(self.angesagt, erwartungswert_wuerfel) is True:
            self.schaue(token)
        else:
            self.würfle(token)

    def differenz_analyse(self, token):
        if self.differenz_der_würfel() >= 6:
            self.würfle(token)
        else:
            self.schaue(token)

    def vorherigeSpieler_analyse(self, token):
        if self.vorherigeSpieler >= 5:
            self.schaue(token)
        else:
            self.würfle(token)

    def schaue(self, token):
        self.schicke_nachricht(Nachrichten.SCHAUEN, [token])

    def würfle(self, token):
        self.schicke_nachricht(Nachrichten.WUERFELN, [token])


if __name__ == "__main__":
    bot = EinfacherBot(server_ip="127.0.0.1", name="janneks_bot")
    bot.starte(automatisch_mitspielen=True)
