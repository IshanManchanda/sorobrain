from random import randint

from django.db import models
from django.utils import timezone


class ReferralCode(models.Model):
    class Meta:
        verbose_name = 'Referral Code'
        verbose_name_plural = 'Referral Codes'

    code = models.CharField('Code', max_length=140, unique=True)
    referrer = models.OneToOneField(to='User', on_delete=models.CASCADE, verbose_name='Referrer')
    used_by = models.ManyToManyField(to='User', verbose_name='Used By', related_name='referee')
    referrer_incentive = models.IntegerField('Referrer Incentive', default=50)
    referee_incentive = models.IntegerField('Referee Incentive', default=50)
    redeemed = models.BooleanField('Redeemed', default=False)
    created = models.DateTimeField("Created On", default=timezone.now)

    @property
    def uses(self) -> int:
        return len(self.used_by.all())

    @staticmethod
    def build_code(user) -> str:
        return f"{user.username.upper()}-{''.join([str(randint(0, 10)) for _ in range(3)])}"

    def use(self, user_using_code):
        self.used_by.add(user_using_code)
        self.save()

        self.referrer.points += self.referrer_incentive
        self.referrer.save()
        user_using_code.points += self.referee_incentive
        user_using_code.save()

        x = user_using_code.referral_code
        x.redeemed = True
        x.save() 
        