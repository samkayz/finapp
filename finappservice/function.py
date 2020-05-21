from finappservice.models import Customer



def customerId():
    last_id = Customer.objects.all().order_by('id').last()
    if not last_id:
        return '1000000000'
    customerId = last_id.customerId
    id_int = int(customerId)
    new_idNo = id_int + 1
    return new_idNo