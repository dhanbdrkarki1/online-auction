from django.utils import timezone
def rename_profile_image(instance, filename):
    lot_id = instance.lot.pk
    current_time = timezone.now().strftime('%Y%m%d%H%M%S')
    ext = filename.split('.')[-1]
    new_filename = f"lots/{timezone.now().strftime('%Y/%m/%d')}/{lot_id}_{current_time}.{ext}"
    return new_filename