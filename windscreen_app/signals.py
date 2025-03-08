from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invoice, StatementOfAccount

@receiver(post_save, sender=Invoice)
def update_statement(sender, instance, **kwargs):
    statement, created = StatementOfAccount.objects.get_or_create(customer_name=instance.customer_name)
    statement.invoices.add(instance)
    statement.update_total_due()
