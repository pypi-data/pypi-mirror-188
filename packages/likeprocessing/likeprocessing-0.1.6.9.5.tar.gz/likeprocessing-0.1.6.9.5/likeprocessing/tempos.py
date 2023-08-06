import likeprocessing.processing as processing


class Tempo:

    def __init__(self, duree_ms: int):
        """t=Tempo(500) créer un objet de temporisation t de durée 500 ms qui se relance indéfiniment"""
        self.depart = processing.frameCount()
        self.duree_ms = duree_ms
        self.__on = False

    def set_tempo(self, duree_ms: int):
        """permet de réinitialiser la temporisation avec une nouvelle valeur."""
        self.depart = processing.frameCount()
        self.duree_ms = duree_ms

    def reset(self):
        """force le redémarrage de la temporisation."""
        self.depart = processing.frameCount()

    def fin(self) -> bool:
        """renvoie True lorsque la temporisation est terminée. Pour notre exemple au bout de 500 ms."""
        if ((processing.frameCount() - self.depart) / processing.getFrameRate()) * 1000 >= self.duree_ms:
            self.depart = processing.frameCount()
            self.__on = not self.__on
            return True
        else:
            return False

    def is_on(self):
        """renvoie True si la temporisation est à on."""
        self.fin()
        return self.__on

    def is_off(self):
        """renvoie True si la temporisation est à off."""
        return not self.is_on()