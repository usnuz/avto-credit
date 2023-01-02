from django.db import models
from django.contrib.auth.models import User
import jsonfield


class Credit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    loan_period = models.IntegerField()
    grace_period = models.IntegerField(default=0)
    interest_rate = models.IntegerField()
    type = models.IntegerField(default=0, choices=(
        (0, 'Annuity'),
        (1, 'Differential')
    ))
    date = models.DateField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now_add=True)
    monthly_payment = jsonfield.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.type == 0:
            main_amount = self.amount
            a = []
            x = 0
            monthly_payment_1 = (self.amount * (self.interest_rate / 12)) / ((1 - (1 + (self.interest_rate / 12))) * (1 - self.loan_period))
            for i in range(self.loan_period):
                monthly_interest_rate = (main_amount * ((self.interest_rate / 100) / 12))
                main_amount -= monthly_payment_1
                x += 1
                a.append({
                    "month": x,
                    "Main amount": (monthly_payment_1 - monthly_interest_rate),
                    "Interest accrued": monthly_interest_rate,
                    "Monthly payment": monthly_payment_1,
                    "Remaining amount": main_amount,
                })
            self.monthly_payment = a
            super(Credit, self).save(*args, **kwargs)
        else:
            main_amount = self.amount
            main_amount_1 = self.amount
            a = []
            x = 0
            for i in range(self.loan_period):
                x += 1
                main_amount_1 -= ((self.amount / self.loan_period) + (main_amount * ((self.interest_rate / 100) / 12)))
                a.append({
                    "month": x,
                    "Main amount": (self.amount / self.loan_period),
                    "Interest accrued": (main_amount * ((self.interest_rate / 100) / 12)),
                    "Monthly payment": ((self.amount / self.loan_period) + (main_amount * ((self.interest_rate / 100) / 12))),
                    "Remaining amount": main_amount_1
                })
                main_amount -= ((self.amount / self.loan_period) + (main_amount * ((self.interest_rate / 100) / 12)))
            self.monthly_payment = a
            super(Credit, self).save(*args, **kwargs)




