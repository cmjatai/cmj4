from django.db import models
from django.utils.translation import gettext_lazy as _


class Teste(models.Model):
    teste = models.CharField(max_length = 100, verbose_name = _('Teste'))

    class Meta:
        verbose_name = _('Teste')
        verbose_name_plural = _("Testes's")
        ordering = ('teste'),

    def __str__(self):
        return self.teste
