from django.utils import timezone
def rename_profile_image(instance, filename):
    current_time = timezone.now().strftime('%Y%m%d%H%M%S')
    ext = filename.split('.')[-1]
    new_filename = f"profiles/{timezone.now().strftime('%Y/%m/%d')}/{current_time}.{ext}"
    return new_filename